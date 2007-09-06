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
"""not specialized generator for configuration files
"""

__version__ = "$Id$"

# phython imports
import logging
from datetime import datetime

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.dublincore.interfaces import IZopeDublinCore
from zope.lifecycleevent import ObjectCreatedEvent
from zope.event import notify
from zope.component import createObject

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.netscan.interfaces import IScanner

logger = logging.getLogger("NetScan")


class Scanner(Supernode):
    """Implementation of unspecified generator
    """

    implements(IScanner)

    def __init__(self):
        Supernode.__init__(self)

    def createObjects(self, dataDict, containerObject):
        """
        will use factories to create the objects from the dataDict
        """
        for host in dataDict:
            dateNow = datetime.utcnow()
            newHost = createObject(u'org.ict_ok.components.host.host.Host')
            notify(ObjectCreatedEvent(newHost))
            containerObject.__setitem__(newHost.getObjectId(), 
                                         newHost)
            dcore = IZopeDublinCore(newHost, None)
            dcore.creators = [u'ikportscan']
            newHost.ikComment += u"scanner: %s" % (dateNow)
            if host.has_key('hostname'):
                newHost.__setattr__("ikName", host['hostname'])
                newHost.__setattr__("hostname", host['hostname'])
                dcore.title = host['hostname']
            else:
                if host.has_key('interfaces'):
                    newHost.__setattr__("ikName", host['interfaces'][0]['ipAddress'])
                    dcore.title = host['interfaces'][0]['ipAddress']
                else:
                    newHost.__setattr__("ikName", u"unknown")
                    newHost.__setattr__("hostname", u"unknown")
                    dcore.title = u"unknown"
                    
            if host.has_key('description'):
                print "description: %s" % host['description']
                newHost.__setattr__("ikDesc", host['description'])
            for my_atrb in ['building', 'room', 'manufacturer', 'vendor',
                            'workinggroup', 'hardware', 'user', 'inv_id']:
                if host.has_key(my_atrb):
                    newHost.__setattr__(my_atrb, host[my_atrb])
            #if host.has_key('building'):
                #newHost.__setattr__("building", host['building'])
            #if host.has_key('room'):
                #newHost.__setattr__("room", host['room'])
            if host.has_key('oss'):
                for i_os in host['oss']:
                    os_string = u"%s %s (%s) (%s)" % (i_os['osfamily'],
                                                      i_os['osgen'],
                                                      i_os['type'],
                                                      i_os['vendor'])
                    newHost.osList.append(os_string)
            newHost.__setattr__("genNagios", True)
            dcore.created = dateNow
                
            if host.has_key("interfaces") and len(host['interfaces'])>0:
                for interfaceDict in host['interfaces']:
                    #print "interfaceDict: ", interfaceDict
                    dateNow = datetime.utcnow()
                    newInterface = zapi.createObject(\
                        u'org.ict_ok.components.interface.interface.Interface')
                    notify(ObjectCreatedEvent(newInterface))
                    newInterfaceId=u"If%s" % (interfaceDict['nbr'])
                    newHost.__setitem__(newInterfaceId, newInterface)
                    #newInterface.__setattr__("description", interfaceDict['name'])
                    #newInterface.__setattr__("ifindex", interfaceDict['nbr'])
                    newInterface.__setattr__("ikName", interfaceDict['name'])
                    newInterface.ikComment += u"scanner: %s" % (dateNow)
                    newInterfaceDc = IZopeDublinCore(newInterface, None)
                    newInterfaceDc.title = u"%s" % interfaceDict['name']
                    newInterfaceDc.created = datetime.utcnow()
                    newInterfaceDc.creators = [u'ikportscan']
                    newInterface.netType = "ethernet"
                    if interfaceDict.has_key('macAddress'):
                        newInterface.mac = interfaceDict['macAddress']
                    if interfaceDict.has_key('ipAddressType') and interfaceDict['ipAddressType'] == 'ipv4' and interfaceDict.has_key('ipAddress'):
                        newInterface.ipv4List.append(interfaceDict['ipAddress'])
                    #### services
                    for service in interfaceDict['services']:
                        newService = zapi.createObject(\
                            u'org.ict_ok.components.service.service.Service')
                        notify(ObjectCreatedEvent(newService))
                        newServiceId=u"%s" % (service['port'])
                        newInterface.__setitem__(newServiceId, newService)
                        newServiceDc = IZopeDublinCore(newService, None)
                        newServiceDc.creators = [u'ikportscan']
                        newServiceDc.created = datetime.utcnow()
                        tmpString = u""
                        if service.has_key('product'):
                            tmpString += service['product'] + u"\n"
                        if service.has_key('version'):
                            tmpString += u"Ver. " + service['version'] + u"\n"
                        if service.has_key('extrainfo'):
                            tmpString += service['extrainfo'] + u"\n"
                        if service.has_key('method'):
                            tmpString += u"scan method: " + service['method'] + u"\n"
                        if len(tmpString) > 0:
                            newService.ikComment += tmpString
                        if service.has_key('service'): ## and (len(port['service']) > 0):
                            newServiceDc.title = u"%s" % service['service']
                            newService.__setattr__("ikName", service['service'])
                        else:
                            newServiceDc.title = u"%s" % service['port']
                        #newHost.__setitem__(newServiceId, newService)
                    #containerObject.__setitem__(new_id, newHost)
                    ### SNMP-Liste aufbauen
                    #if interfaceDict.has_key("snmplist") and len(interfaceDict['snmplist'])>0:
                        #for snmpDict in interfaceDict['snmplist']:
                            ### oid-Test
                            #newSnmp = zapi.createObject(None, 'ikom.iksnmp.IkSnmp')
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
            ####portsInterface = zapi.createObject(\
                ####u'org.ikomtrol.ikinterface.ikinterface.IkInterface')
            ####notify(ObjectCreatedEvent(portsInterface))
            ####newHost.__setitem__(portsInterface.getObjectId(), 
                                ####portsInterface)
            ####newInterfaceDc = IZopeDublinCore(portsInterface, None)
            ####newInterfaceDc.title = u"If10000"
            ####portsInterface.__setattr__("ikName", u"If10000")
            ####newInterfaceDc.created = dateNow
            ####newInterfaceDc.creators = [u'ikportscan']
            ####portsInterface.ikComment += u"scanner: %s" % (dateNow)
            ####portsInterface.ipv4List.append(host['ipAddress'])
            ####portsInterface.netType = 'ethernet'
            ####if host.has_key('macAddress'):
                ####portsInterface.mac = host['macAddress']
                
        return None
