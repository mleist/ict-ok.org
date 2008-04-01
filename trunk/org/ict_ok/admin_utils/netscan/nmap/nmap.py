# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=E1101,E0611
#
"""Configuration adapter for nmap-config files
"""

__version__ = "$Id$"

# phython imports
import logging
from datetime import datetime
from pytz import timezone
from lxml import etree
from pprint import pprint

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.lifecycleevent import ObjectCreatedEvent
from zope.dublincore.interfaces import IZopeDublinCore
from zope.event import notify
from zope.component import createObject

# ict_ok.org imports
from org.ict_ok.admin_utils.netscan.scanner import \
     Scanner
from org.ict_ok.admin_utils.netscan.nmap.interfaces import \
     IAdmUtilNMap

logger = logging.getLogger("AdmUtilNMap")
berlinTZ = timezone('Europe/Berlin')


class AdmUtilNMap(Scanner):
    """Implementation of nmap scanner wrapper
    """

    implements(IAdmUtilNMap)

    def __init__(self):
        super(AdmUtilNMap, self).__init__()
        self.ikRevision = __version__

    def buildDataDict(self, ipAddressStr):
        """
        fill our data dictonary
        """
        f = open("/home/sebastian/Desktop/drako.xml", "r")
        xmlstring = f.read()
        f.close()
        tree = etree.fromstring(xmlstring)
        nmaprun = tree.getchildren()
        
        returnList = []
        for host in nmaprun:
            if(host.tag == "host"):
                hostDict = {}
                for address in host.findall('address'):
                    if(address.attrib['addrtype'] == 'ipv4'):
                        ip = address.attrib['addr']
                    elif(address.attrib['addrtype'] == 'mac'):
                        mac = address.attrib['addr']
                hostDict['hostname'] = unicode(ip)
                hostnames = host.find('hostnames')
                hostnameschilds = hostnames.getchildren()
                if(len(hostnameschilds) > 0):
                    hostname = hostnameschilds[0].get('name')
                    hostDict['hostname'] = unicode(hostname)
                hostDict['description'] = u''
                hostDict['manufacturer'] = u''
                hostDict['vendor'] = u''
                hostDict['workinggroup'] = u''
                hostDict['hardware'] = u''
                hostDict['user'] = u''
                hostDict['inv_id'] = u''
                hostDict['building'] = u''
                hostDict['room'] = u''
                hostDict['oss'] = []
                hostDict['interfaces'] = [
                    {
                        'nbr': u'01',
                        'name': u'lan01',
                        'netType': u'ethernet',
                        'macAddress': mac,
                        'ipAddress': ip,
                        'ipAddressType': u'ipv4',
                        'services': []
                    }
                ]
        
        # service
        #{
                #'port': u''
                #'product': u''
                #'version': u''
                #'extrainfo': u''
                #'method': u''
                #'service': u''
            #}
                #import pdb
                #pdb.set_trace()
                for ports in host.findall('ports'):
                    for port in ports.findall('port'):
                        serviceDict = {}
                        serviceDict['port'] = port.attrib['portid']
                        serviceDict['protocol'] = port.attrib['protocol']
                        for child in port.getchildren():
                            if(child.tag == 'service'):
                                serviceDict['service'] = child.attrib['name']
                                try:
                                    serviceDict['product'] = child.attrib['product']
                                except:
                                    serviceDict['product'] = u''
                        hostDict['interfaces'][0]['services'].append(serviceDict)
                returnList.append(hostDict)
        return returnList

    def createServiceObject(self, parent, serviceDict):
        """helper methode to create service instance
        """
        dateNow = datetime.utcnow()
        #if port['port'] == u"389":   ## ldap
            #newService = zapi.createObject(None, 'ikom.service.ServiceLdap')
            #newService.__setattr__("basedn", u'dc=domain,dc=tld')
        if False:
            pass
        elif serviceDict['port'] == u"22":   ## ssh
            newService = zapi.createObject(\
                u'org.ict_ok.components.service.special.ssh.service.ServiceSsh')
        elif serviceDict['port'] == u"80":   ## ssh
            newService = zapi.createObject(\
                u'org.ict_ok.components.service.special.http.service.ServiceHttp')
        else:
            newService = zapi.createObject(\
                u'org.ict_ok.components.service.service.Service')
        newServiceId=u"%s" % (serviceDict['port'])
        parent.__setitem__(newService.getObjectId(), newService)
        #newService.__setattr__("genNagios", True)
        newServiceDc = IZopeDublinCore(newService, None)
        newServiceDc.title = u"%s" % serviceDict['service']
        newServiceDc.created = datetime.utcnow()
        newServiceDc.creators = [u'ikportscan']
        try:
            intPort = int(serviceDict['port'])
            newService.__setattr__("port", intPort)
        except ValueError:
            raise Exception, "port number isn't valid '%s'" % serviceDict['port']
        except TypeError:
            raise Exception, "port number isn't valid '%s'" % serviceDict['port']
        newService.__setattr__("product", unicode(serviceDict['product']))
        newService.__setattr__("ipprotocol",
                               unicode(serviceDict['protocol'.lower()]))
        if serviceDict.has_key('service'): ## and (len(port['service']) > 0):
            newServiceDc.title = u"%s" % serviceDict['service']
        else:
            newServiceDc.title = u"%s" % serviceDict['port']
        notify(ObjectCreatedEvent(newService))

    def createInterfaceObject(self, parent, interfaceDict):
        """helper methode to create interface instance
        """
        dateNow = datetime.utcnow()
        newInterface = createObject(\
            u'org.ict_ok.components.interface.interface.Interface')
        newInterfaceId=u"If%s" % (interfaceDict['nbr'])
        parent.__setitem__(newInterface.getObjectId(), newInterface)
        newInterfaceDc = IZopeDublinCore(newInterface, None)
        newInterfaceDc.title = u"%s" % interfaceDict['name']
        newInterfaceDc.__setattr__("ikName", newInterfaceDc.title)
        newInterfaceDc.created = datetime.utcnow()
        newInterfaceDc.creators = [u'ikportscan']
        newInterface.ikComment += u"scanner: %s" % (dateNow)
        if interfaceDict.has_key('macAddress'):
            newInterface.__setattr__("mac", unicode(interfaceDict['macAddress']))
        if interfaceDict.has_key('ipAddressType') and \
           interfaceDict['ipAddressType'] == u'ipv4':
            if interfaceDict.has_key('ipAddress'):
                #newInterface.ipv4List.append(interfaceDict['ipAddress'])
                newInterface.ipv4List = unicode(interfaceDict['ipAddress'])
        ### build snmp objects
        #if interfaceDict.has_key("snmplist") and len(interfaceDict['snmplist'])>0:
            #for snmpDict in interfaceDict['snmplist']:
                ### oid-Test
                #newSnmp = zapi.createObject(None, 'ikom.snmp.Snmp')
                #notify(ObjectCreatedEvent(newSnmp))
                #newSnmp.__setattr__("description", snmpDict['name'])
                #newSnmp.__setattr__("checktype", "oid")
                #newSnmp.__setattr__("inputtype", "abs")
                #newSnmp.__setattr__("oid1", snmpDict['oid1'])
                #newSnmp.__setattr__("oid2", snmpDict['oid2'])
                #for i in ["cmd", "inptype", "inpUnit", "displayUnitNumerator", "displayUnitDenominator",
                          #"checkMax", "checkMaxLevel", "checkMaxLevelUnitNumerator", "checkMaxLevelUnitDenominator"]:
                    #newSnmp.__setattr__(i, snmpDict[i])
                #newSnmpDc = IZopeDublinCore(newSnmp, None)
                #newSnmpId=u"%s" % (snmpDict['name'])
                #newSnmpDc.title = u"%s" % (snmpDict['name'])
                #newSnmpDc.created = datetime.utcnow()
                #newSnmpDc.creators = [u'ikportscan']
                #newInterface.__setitem__(newSnmpId, newSnmp)
        ### build services
        for serviceDict in interfaceDict['services']:
            self.createServiceObject(newInterface, serviceDict)
        notify(ObjectCreatedEvent(newInterface))

    def createHostObject(self, parent, hostDict):
        """helper methode to create host instance
        """
        dateNow = datetime.utcnow()
        newHost = createObject(u'org.ict_ok.components.host.host.Host')
        notify(ObjectCreatedEvent(newHost))
        parent.__setitem__(newHost.getObjectId(), 
                           newHost)
        dc = IZopeDublinCore(newHost, None)
        dc.creators = [u'ikportscan']
        newHost.ikComment += u"scanner: %s" % (dateNow)
        if hostDict.has_key('hostname'):
            newHost.__setattr__("ikName", hostDict['hostname'])
            newHost.__setattr__("hostname", hostDict['hostname'])
            dc.title = hostDict['hostname']
        else:
            newHost.__setattr__("ikName", hostDict['ipAddress'])
            dc.title = hostDict['ipAddress']
        for i_os in hostDict['oss']:
            os_string = u"%s %s (%s) (%s)" % (i_os['osfamily'],
                                               i_os['osgen'],
                                               i_os['type'],
                                               i_os['vendor'])
            newHost.osList.append(os_string)
        newHost.__setattr__("genNagios", True)
        dc.created = dateNow
        if hostDict.has_key("interfaces") and len(hostDict['interfaces'])>0:
            for interfaceDict in hostDict['interfaces']:
                self.createInterfaceObject(newHost, interfaceDict)
        notify(ObjectCreatedEvent(newHost))

    def createObjects(self, hostList, containerObject):
        """
        will use factories to create the objects from the dataDict
        """
        for hostDict in hostList:
            self.createHostObject(containerObject, hostDict)
        return None

    def startScan(self, networkObj):
        """
        fills the network object with data
        """
        ipAddress = networkObj.ipv4
        dataDict = self.buildDataDict(ipAddress)
        self.createObjects(dataDict, networkObj)
        pprint(dataDict)
