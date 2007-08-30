# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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
import xml.dom.minidom
from datetime import datetime
from pytz import timezone
from xml.dom.minidom import Node
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
        doc = xml.dom.minidom.parse("/home/markus/Projekte/python_nmap/3.xml")
        hosts = doc.getElementsByTagName('host')
        resultList = []
        
        for host in hosts:
            try:
                del(result)
            except:
                pass
            result = {}        
            if host.nodeType == Node.ELEMENT_NODE:
                hostStatusElements = host.getElementsByTagName('status')
                if hostStatusElements[0].hasAttribute('state'):
                    hostState = hostStatusElements[0].getAttribute('state')
                    if hostState == 'up':
                        ####### Hostinformation
                        hostAddressElements = host.getElementsByTagName('address')
                        for addressElement in hostAddressElements:
                            addressType = addressElement.getAttribute('addrtype')
                            if addressType == 'ipv4':
                                result['ipAddress'] =  addressElement.getAttribute('addr')
                                result['pAddressType'] = addressElement.getAttribute('addrtype')
                            if addressType == 'mac':
                                result['macAddress'] =  addressElement.getAttribute('addr')
                        hostNameElements = host.getElementsByTagName('hostname')
                        if len(hostNameElements) > 0:
                            result['hostname'] = hostNameElements[0].getAttribute('name')
                        ####### Portinformation
                        result['ports'] = []
                        hostPorts = host.getElementsByTagName('port')
                        for hostPort in hostPorts:
                            portStatusElements = hostPort.getElementsByTagName('state')
                            if portStatusElements[0].getAttribute('state').find("open") >= 0 : # cause of 'open|filtered'
                                portServiceElements = hostPort.getElementsByTagName('service')
                                try:
                                    del(resultPort)
                                except:
                                    pass
                                resultPort = {}
                                resultPort['port'] = hostPort.getAttribute('portid')
                                resultPort['state'] = portStatusElements[0].getAttribute('state')
                                resultPort['protocol'] = hostPort.getAttribute('protocol')
                                if len(portServiceElements) > 0:
                                    resultPort['service'] =  portServiceElements[0].getAttribute('name')
                                else:
                                    resultPort['service'] = "Port %s" % resultPort['port']
                                result['ports'].append(resultPort)
                        ####### Operatingsystem information
                        result['oss'] = []
                        hostOss = host.getElementsByTagName('osclass')
                        for hostOs in hostOss:
                            try:
                                del(resultOs)
                            except:
                                pass
                            resultOs = {}
                            resultOs['type'] = hostOs.getAttribute('type')
                            resultOs['vendor'] = hostOs.getAttribute('vendor')
                            resultOs['osfamily'] = hostOs.getAttribute('osfamily')
                            resultOs['osgen'] = hostOs.getAttribute('osgen')
                            resultOs['accuracy'] = hostOs.getAttribute('accuracy')
                            result['oss'].append(resultOs)
                        resultList.append(result)
        return resultList

    def createObjects(self, dataDict, containerObject):
        """
        will use factories to create the objects from the dataDict
        """
        for host in dataDict:
            dateNow = datetime.now(berlinTZ)
            newHost = createObject(u'org.ict_ok.components.host.host.Host')
            notify(ObjectCreatedEvent(newHost))
            containerObject.__setitem__(newHost.getObjectId(), 
                                         newHost)
            dc = IZopeDublinCore(newHost, None)
            dc.creators = [u'ikportscan']
            newHost.ikComment += u"scanner: %s" % (dateNow)
            if host.has_key('hostname'):
                newHost.__setattr__("ikName", host['hostname'])
                newHost.__setattr__("hostname", host['hostname'])
                dc.title = host['hostname']
            else:
                newHost.__setattr__("ikName", host['ipAddress'])
                dc.title = host['ipAddress']
            for i_os in host['oss']:
                os_string = u"%s %s (%s) (%s)" % (i_os['osfamily'],
                                                   i_os['osgen'],
                                                   i_os['type'],
                                                   i_os['vendor'])
                newHost.osList.append(os_string)
            newHost.__setattr__("genNagios", True)
            dc.created = dateNow
                
            if host.has_key("interfaces") and len(host['interfaces'])>0:
                for interfaceDict in host['interfaces']:
                    newInterface = zapi.createObject(\
                        u'org.ict_ok.components.interface.interface.Interface')
                    notify(ObjectCreatedEvent(newInterface))
                    newInterfaceId=u"If%s" % (interfaceDict['nbr'])
                    newHost.__setitem__(newInterfaceId, newInterface)
                    #newInterface.__setattr__("description", interfaceDict['name'])
                    #newInterface.__setattr__("ifindex", interfaceDict['nbr'])
                    newInterfaceDc = IZopeDublinCore(newInterface, None)
                    newInterfaceDc.title = u"%s" % interfaceDict['name']
                    newInterfaceDc.created = datetime.utcnow()
                    newInterfaceDc.creators = [u'ikportscan']
                    ### SNMP-Liste aufbauen
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
                    #newHost.__setitem__(newInterfaceId, newInterface)

            #if host.has_key("building"):
                #newHost.__setattr__("building", host['building'])

            #if host.has_key('oss') and len(host['oss'])>0:
                #hostOs = host['oss'][0]
                #firstOs = "%s - %s - %s - %s - %s" % (hostOs['vendor'],hostOs['osfamily'],hostOs['osgen'],hostOs['accuracy'],hostOs['type'])
                #newHost.__setattr__("os", firstOs)
            #else:
                #newHost.__setattr__("os", u"unknown")
                
            ### add services to interface if1
            ####### Interface
            portsInterface = zapi.createObject(\
                u'org.ict_ok.components.interface.interface.Interface')
            notify(ObjectCreatedEvent(portsInterface))
            newHost.__setitem__(portsInterface.getObjectId(), 
                                portsInterface)
            newInterfaceDc = IZopeDublinCore(portsInterface, None)
            newInterfaceDc.title = u"If10000"
            portsInterface.__setattr__("ikName", u"If10000")
            newInterfaceDc.created = dateNow
            newInterfaceDc.creators = [u'ikportscan']
            portsInterface.ikComment += u"scanner: %s" % (dateNow)
            portsInterface.ipv4List.append(host['ipAddress'])
            portsInterface.netType = 'ethernet'
            if host.has_key('macAddress'):
                portsInterface.mac = host['macAddress']
                
            for port in host['ports']:
                #if port['protocol'].lower() == "tcp":
                    #print "tcp"
                #elif port['protocol'].lower() == "udp":
                    #print "udp"
                #if port['port'] == u"389":   ## ldap
                    #newService = zapi.createObject(None, 'ikom.service.ServiceLdap')
                    #notify(ObjectCreatedEvent(newService))
                    #newService.__setattr__("basedn", u'dc=domain,dc=tld')
                #elif port['port'] == u"1111180":   ## http
                    #pass
                #else:
                    #newService = zapi.createObject(None, 'ikom.service.Service')
                    #notify(ObjectCreatedEvent(newService))
                newService = zapi.createObject(\
                    u'org.ict_ok.components.service.service.Service')
                notify(ObjectCreatedEvent(newService))
                newServiceId=u"%s" % (port['port'])
                portsInterface.__setitem__(newServiceId, newService)
                #newService.__setattr__("genNagios", True)
                newServiceDc = IZopeDublinCore(newService, None)
                #newService.__setattr__("port", port['port'])
                #newService.__setattr__("protocol", port['protocol'])
                #newService.__setattr__("description", port['service'])
                newServiceDc.creators = [u'ikportscan']
                newServiceDc.created = datetime.utcnow()
                if port.has_key('service'): ## and (len(port['service']) > 0):
                    newServiceDc.title = u"%s" % port['service']
                else:
                    newServiceDc.title = u"%s" % port['port']
                #newHost.__setitem__(newServiceId, newService)
            #containerObject.__setitem__(new_id, newHost)
        return None
        

    def startScan(self, networkObj):
        """
        fills the network object with data
        """
        ipAddress = networkObj.ipv4
        dataDict = self.buildDataDict(ipAddress)
        self.createObjects(dataDict, networkObj)
        pprint(dataDict)
