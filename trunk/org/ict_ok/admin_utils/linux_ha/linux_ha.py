# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""implementation of a "linux_ha daemon" 
"""

__version__ = "$Id$"

# python imports
import logging
from datetime import datetime

# zope imports
from zope.interface import implements
from zope.component import adapter
from zope.i18nmessageid import MessageFactory
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.app.container.interfaces import IReadContainer
from zope.schema.fieldproperty import FieldProperty
from zope.component import createObject
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.linux_ha.interfaces import IAdmUtilLinuxHa
from org.ict_ok.admin_utils.linux_ha.interfaces import IGlobalLinuxHaUtility
from org.ict_ok.admin_utils.linux_ha.connection import LinuxHaConnectionThread
from zope.app.container.contained import contained

logger = logging.getLogger("AdmUtilLinuxHa")
_ = MessageFactory('org.ict_ok')

from zope.annotation.interfaces import IAnnotations

class AdmUtilLinuxHa(Supernode):
    """Implementation of local LinuxHa Utility"""

    implements(IAdmUtilLinuxHa, IReadContainer, IAnnotations)

    linuxHaServerActive = FieldProperty(IAdmUtilLinuxHa['linuxHaServerActive'])
    linuxHaServerIp = FieldProperty(IAdmUtilLinuxHa['linuxHaServerIp'])
    linuxHaServerPort = FieldProperty(IAdmUtilLinuxHa['linuxHaServerPort'])
    linuxHaUsername = FieldProperty(IAdmUtilLinuxHa['linuxHaUsername'])
    linuxHaPassword = FieldProperty(IAdmUtilLinuxHa['linuxHaPassword'])

    lastLinuxHa = "no signal since start"

    def __init__(self):
        print "AdmUtilLinuxHa.__init__"
        Supernode.__init__(self)
        self.connState = u"never connected"
        #self.apiFullName = u"never get API"
        self.ikRevision = __version__

    def connect2HaCluster(self):
        if self.linuxHaServerActive:
            print "#-> AdmUtilLinuxHa.connect2VimServer: ", self.getObjectId()
            globalLinuxHaUtility.connectToLinuxHa(self)

    def getNodes(self):
        """ list of all cluster nodes objects
        """
        return globalLinuxHaUtility.getNodes(self)
    
    def updateConnState(self):
        """update the connection state with timestamp
        """
        if self.linuxHaServerActive:
            self.connState = str(datetime.utcnow())

    #def setConnStatus(self, connString):
        #if self.connStatus != connString:
            #self.connStatus = connString
            #self._p_changed = True

    def __getitem__(self, key):
        '''See interface `IReadContainer`'''
        if self.linuxHaServerActive:
            print "AdmUtilLinuxHa.__getitem__(%s)" % (key)
            if self.has_key(key):
                return self[key]
            myDict = self.tempNodeGenerator()
            if myDict.has_key(key):
                return myDict[key]
            raise KeyError
        else:
            return None

    def __getattr__(self, key):
        if self.linuxHaServerActive:
            print "AdmUtilLinuxHa.__getattr__(%s)" % (key)
            if self.has_key(key):
                return self[key]
            myDict = self.tempNodeGenerator()
            if myDict.has_key(key):
                return myDict[key]
            if key == '__annotations__':
                return None
            if key == '__getnewargs__':
                return None
            raise KeyError
        else:
            return None

    def values(self):
        '''See interface `IReadContainer`'''
        if self.linuxHaServerActive:
            print "AdmUtilLinuxHa.values"
            return self.tempNodeGenerator().values()
            #Supernode.values(self)
            #return globalLinuxHaUtility.get_LinuxHaDatacenter_values(self)
            #return globalLinuxHaUtility.get_LinuxHaDatacenter_Dict(self, self).values()
            #return globalLinuxHaUtility.get_LinuxHaAllDict(self, self).values()
            #return getTestDict(self).values()
        else:
            return None

    def tempNodeGenerator(self):
        print "tempNodeGenerator"
        retDict = {}
        parentObj = self
        for i in range(25):
            iname = u"Name %d" % i
            # Node 1
            newNodeObj = createObject(\
                "org.ict_ok.admin_utils.linux_ha.linux_ha_node.LinuxHaObjNode")
            newNodeObj.name = iname
            contained(newNodeObj, parentObj, iname)
            newNodeObj.__parent__ = parentObj
            retDict[iname] = newNodeObj
        ## Node 2
        #newNodeObj = createObject(\
            #"org.ict_ok.admin_utils.linux_ha.linux_ha_node.LinuxHaObjNode")
        #newNodeObj.name = u'Node xyz2'
        #contained(newNodeObj, parentObj, u'Node xyz2')
        #newNodeObj.__parent__ = parentObj
        #retDict[u"Node xyz2"] = newNodeObj
        return retDict

    #def keys(self):
        #print "AdmUtilLinuxHa.keys"
        #Supernode.keys(self)

    #def __iter__(self):
        #print "AdmUtilLinuxHa.__iter__"
        #Supernode.__iter__(self)

    #def get(self, key, default=None):
        #print "AdmUtilLinuxHa.get(%s,%s)" % (key, default)
        #Supernode.get(self, key, default)


    #def __len__(self):
        #print "AdmUtilLinuxHa.__len__"
        #Supernode.__len__(self)

    #def items(self):
        #print "AdmUtilLinuxHa.items"
        #Supernode.items(self)

    #def __contains__(self, key):
        #print "AdmUtilLinuxHa.__contains__(%s)" % (key)
        #Supernode.__contains__(self, key)
        
        
        
    #def powerOffVm(self, uuid):
        #return globalLinuxHaUtility.powerOffVm(uuid, self)

    #def powerOnVm(self, uuid):
        #return globalLinuxHaUtility.powerOnVm(uuid, self)

    #def shutdownHostEsxHost(self, esxName):
        #return globalLinuxHaUtility.shutdownHostEsxHost(esxName, self)

    #def enterMaintenanceModeEsxHost(self, esxName):
        #return globalLinuxHaUtility.enterMaintenanceModeEsxHost(esxName, self)

    #def get_LinuxHaObject_Dict(self, myParams, parentObj):
        #return globalLinuxHaUtility.get_LinuxHaObject_Dict(myParams,
                                                         #parentObj)

    #def getEsxRoomUuid(self, uuid):
        #return globalLinuxHaUtility.getEsxRoomUuid(uuid, self)

    #def receiveLinuxHa(self, request, str_time, mode=None):
        #"""receive linux_ha signal
        #"""
        #logger.info(u"AdmUtilLinuxHa::receiveLinuxHa(%s, %s) in '%s'" \
                    #% (str_time, mode,zapi.getPath(self)))
        #self.lastLinuxHa = str_time
        #dcore = IWriteZopeDublinCore(self)
        #dcore.modified = datetime.utcnow()

    #def getLinuxHaTime(self):
        #"""get last linux_ha timestamp
        #"""
        #try:
            #retVal = self.lastLinuxHa
        #except NameError:
            #self.__setattr__("lastLinuxHa", "not set")
            #retVal = self.lastLinuxHa
        #return retVal


class GlobalLinuxHaUtility(object):

    implements(IGlobalLinuxHaUtility)

    #lastLinuxHa = "no signal since start"

    def __init__(self):
        logger.info(u"GlobalLinuxHaUtility started")
        super(GlobalLinuxHaUtility, self).__init__(self)
        self.subscriber_list = []
        self.connection_dict = {}
        #self.haThread = None
        self.haThread = LinuxHaConnectionThread()
        self.haThread.globalLinuxHa = self
        self.haThread.setDaemon(0)
        self.haThread.start()
        self.timeStarted = datetime.utcnow()
        self.ikRevision = __version__

    #def getUtilityVersion(self):
        #""" global und svn Version of Utility """
        #return "ddd - ", GlobalLinuxHaUtility.lastLinuxHa, " - ", \
               #"Ver0.1"," - ", self.ikRevision, " - eee"

    #def getUptime(self):
        #"""uptime of Utility"""
        #return datetime.utcnow() - self.timeStarted

    #def subscribeToLinuxHa(self, obj):
        ##logger.info(u"GlobalLinuxHaUtility::subscribe2linux_ha(%s)" % obj)
        #if obj not in self.subscriber_list:
            #self.subscriber_list.append(obj)
            ##self.connection_dict[obj.getObjectId()] = None

    #def unsubscribeFromLinuxHa(self, obj):
        ##logger.info(u"GlobalLinuxHaUtility::unsubscribeFromLinuxHa(%s)" % obj)
        #if obj in self.subscriber_list:
            #self.subscriber_list.remove(obj)
            ##del self.connection_dict[obj.getObjectId()]

    def connectToLinuxHa(self, obj):
        #logger.info(u"GlobalLinuxHaUtility::connectToLinuxHa(%s)" % obj)
        if obj.linuxHaServerActive:
            localHaUtilOId = obj.objectID
            connection = {}
            connection['con'] = None
            connection['ip'] = obj.linuxHaServerIp
            connection['port'] = obj.linuxHaServerPort
            connection['username'] = obj.linuxHaUsername
            connection['password'] = obj.linuxHaPassword
            print "connection: %s" % (connection)
            if not connection['con']:
                print "make con"
                myParams = {\
                    'cmd': 'make_con',
                    'admUtilLinuxHaOid': localHaUtilOId,
                    'conn_params': connection
                }
                self.haThread.getQueue(localHaUtilOId)['in'].join()
                self.haThread.getQueue(localHaUtilOId)['in'].put(myParams, True, 15)
                self.haThread.getQueue(localHaUtilOId)['in'].join()
                if self.haThread.getQueue(localHaUtilOId)['out'].qsize() > 0:
                    obj.updateConnState()
                    retValue = self.haThread.getQueue(localHaUtilOId)['out'].get(True, 15)
                    self.haThread.getQueue(localHaUtilOId)['out'].task_done()
                    print "done -> retValue: ", retValue
                #if not self.haThread:
                    #self.haThread = LinuxHaConnectionThread()
                    #self.haThread.globalLinuxHa = self
                    #self.haThread.createQueue(obj.getObjectId())
##                    self.haThread.localLinuxHa = obj
                    #self.haThread.setDaemon(0)
                    #self.haThread.start()
                #else:
                    #print "haThread already active?"
                ##perl.require("VMware::VIM2Runtime")
                ##perl.require("VMware::VILib")
                ##perl.call("Vim::login",
                            ##service_url = "https://192.168.154.10:443/sdk/webService",
                            ##user_name="ikom.trol",
                            ##password="ikom.trol")
            else:
                print "check con if already up"
        print "localHaUtilOId: ", localHaUtilOId
        if self.haThread is None:
            return {}
        myParams = {\
            'cmd': 'xyz',
            'admUtilLinuxHaOid': localHaUtilOId
        }
        self.haThread.getQueue(localHaUtilOId)['in'].join()
        self.haThread.getQueue(localHaUtilOId)['in'].put(myParams, True, 15)
        self.haThread.getQueue(localHaUtilOId)['in'].join()
        if self.haThread.getQueue(localHaUtilOId)['out'].qsize() > 0:
            retList = self.haThread.getQueue(localHaUtilOId)['out'].get(True, 15)
            self.haThread.getQueue(localHaUtilOId)['out'].task_done()
            print "done: ", retList
        print "dont total"
                
    def getNodes(self, obj):
        logger.info(u"GlobalLinuxHaUtility::getNodes(%s)" % obj)
        if obj.linuxHaServerActive:
            localHaUtilOId = obj.objectID
            myParams = {\
                'cmd': 'get_nodes',
                'admUtilLinuxHaOid': localHaUtilOId
                }
            self.haThread.getQueue(localHaUtilOId)['in'].join()
            self.haThread.getQueue(localHaUtilOId)['in'].put(myParams, True, 15)
            self.haThread.getQueue(localHaUtilOId)['in'].join()
            if self.haThread.getQueue(localHaUtilOId)['out'].qsize() > 0:
                obj.updateConnState()
                nodeList = self.haThread.getQueue(localHaUtilOId)['out'].get(True, 15)
                self.haThread.getQueue(localHaUtilOId)['out'].task_done()
                print "done -> nodeList: ", nodeList
                return nodeList
        return None
        
    #def get_LinuxHaDatacenter_keys(self, localEsxUtil):
        #print "IkGlobalLinuxHaUtility.get_LinuxHaDatacenter_keys(%s,%s)" % \
              #(self, localEsxUtil)
        #return []

    #def get_LinuxHaDatacenter_getitem(self, localEsxUtil, key):
        #print "IkGlobalLinuxHaUtility.get_LinuxHaDatacenter_getitem(%s,%s,%s)" % \
              #(self, localEsxUtil, key)
        #return None

    #def get_LinuxHaDatacenter_values(self, localEsxUtil):
        #print "IkGlobalLinuxHaUtility.get_LinuxHaDatacenter_values(%s,%s)" % \
              #(self, localEsxUtil)
        #return []

    #def get_LinuxHaAllDict(self, localEsxUtil, parentObj):
        #retDict = {}

        #objFolder = createObject(\
            #"org.ict_ok.admin_utils.linux_ha.linux_ha_folder.LinuxHaFolder")
        #objFolder.localEsxUtil = localEsxUtil
        #objFolder.name = u'Datacenters'
        #objFolder.esxObjectTypes = r'Datacenter'
        #contained(objFolder, parentObj, u'Datacenters')
        #objFolder.__parent__ = parentObj
        #retDict[u"Datacenters"] = objFolder

        #objFolder = createObject(\
            #"org.ict_ok.admin_utils.linux_ha.linux_ha_folder.LinuxHaFolder")
        #objFolder.localEsxUtil = localEsxUtil
        #objFolder.name = u'HostSystems'
        #objFolder.esxObjectTypes = r'HostSystem'
        #contained(objFolder, parentObj, u'HostSystems')
        #objFolder.__parent__ = parentObj
        #retDict[u'HostSystems'] = objFolder

        #objFolder = createObject(\
            #"org.ict_ok.admin_utils.linux_ha.linux_ha_folder.LinuxHaFolder")
        #objFolder.localEsxUtil = localEsxUtil
        #objFolder.name = u'VirtualMachines'
        #objFolder.esxObjectTypes = r'VirtualMachine'
        #contained(objFolder, parentObj, u'VirtualMachines')
        #objFolder.__parent__ = parentObj
        #retDict[u'VirtualMachines'] = objFolder

        #objFolder = createObject(\
            #"org.ict_ok.admin_utils.linux_ha.linux_ha_folder.LinuxHaFolder")
        #objFolder.localEsxUtil = localEsxUtil
        #objFolder.name = u'Folder'
        #objFolder.esxObjectTypes = r'Folder'
        #contained(objFolder, parentObj, u'Folder')
        #objFolder.__parent__ = parentObj
        #retDict[u'Folder'] = objFolder
        #return retDict


    #def get_LinuxHaObject_Dict(self, myParams, parentObj):
        #""" TODO: caching here please
        #"""
        ##print "get_LinuxHaDatacenter_Dict"
        #if self.haThread is None:
            #return {}
        #localEsxUtil = myParams['admUtilLinuxHa']
        #utilOId = localEsxUtil.getObjectId()
        ##print "aa12"
        ##myParams = {\
            ##'cmd': 'find_entity_views',
            ##'view_type': 'Datacenter',
            ##'admUtilLinuxHa': localEsxUtil,
            ##}
        ##print "aa0a"
        #if self.haThread.getQueue(utilOId)['in'].join():
            #pass
            ##print "aa0b"
        ##print "aa1"
        #self.haThread.getQueue(utilOId)['in'].put(myParams, True, 15)
        ##print "aa2"
        ##print "aa13:", utilOId
        #self.haThread.getQueue(utilOId)['in'].join()
        ##print "aa3"
        ##print "aa14"
        ##self.haThread.queue1_in.put(localEsxUtil, True, 5)
        ##self.haThread.queue1_in.join()
        #esxObjList = self.haThread.getQueue(utilOId)['out'].get(True, 15)
        ##print "aa4"
        ##print "esxObjList: ", esxObjList
        ##print "aa15"
        #self.haThread.getQueue(utilOId)['out'].task_done()
        #if len(esxObjList) == 0:
            #return None
        ##print "aa5"
        ##print "aa16"
        #retDict = {}
        #for esxObj in esxObjList:
            ##print "datacenter0123:", datacenter
            #newObj = None
            #if esxObj['esxType'] == 'Datacenter':
                #newObj = createObject(\
                    #"org.ict_ok.admin_utils.linux_ha.linux_ha_datacenter.LinuxHaDatacenter")
            #elif esxObj['esxType'] == 'HostSystem':
                #newObj = createObject(\
                    #"org.ict_ok.admin_utils.linux_ha.linux_ha_hostsystem.LinuxHaHostSystem")
            #elif esxObj['esxType'] == 'VirtualMachine':
                #newObj = createObject(\
                    #"org.ict_ok.admin_utils.linux_ha.linux_ha_virtual_machine.LinuxHaVirtualMachine")
            #elif esxObj['esxType'] == 'Folder':
                #newObj = createObject(\
                    #"org.ict_ok.admin_utils.linux_ha.linux_ha_folder.LinuxHaFolder")
            #if newObj:
                #contained(newObj, parentObj, esxObj['name'])
                #newObj.localEsxUtil = localEsxUtil
                #newObj.overallStatus = esxObj['overallStatus']
                #newObj.name = esxObj['name']
                #newObj.uuid = esxObj['uuid']
                #if esxObj.has_key('perlRef'):
                    #newObj.perlEsxObjRef = esxObj['perlRef']
                #newObj.__parent__ = parentObj
                #retDict[esxObj['name']] = newObj
        #return retDict

    #def powerOffVm(self, uuid, localEsxUtil):
        #print "powerOffVm"
        #localEsxUtilOId = localEsxUtil.objectID
        #if self.haThread is None:
            #return {}
        #myParams = {\
            #'cmd': 'find_entity_views',
            #'admUtilLinuxHa': localEsxUtil,
            #'view_type': 'VirtualMachine',
            #'filter': {'config.uuid':uuid},
        #}
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #self.haThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #if self.haThread.getQueue(localEsxUtilOId)['out'].qsize() > 0:
            #esxObjList = self.haThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
            #self.haThread.getQueue(localEsxUtilOId)['out'].task_done()
            #if len(esxObjList) == 0:
                #return None
            #esxObj = esxObjList[0]
            #myParams = {\
                #'admUtilLinuxHa': localEsxUtil,
                #'cmd': 'call_fcnt_on_obj',
                #'perlRef': esxObj['perlRef'],
                #'fnct_name': 'ShutdownGuest',
                #'fnct_args': {},
            #}
            #self.haThread.getQueue(localEsxUtilOId)['in'].join()
            #self.haThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
            #self.haThread.getQueue(localEsxUtilOId)['in'].join()
            #if self.haThread.getQueue(localEsxUtilOId)['out'].qsize() > 0:
                #esxObjList = self.haThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
                #self.haThread.getQueue(localEsxUtilOId)['out'].task_done()


    #def powerOnVm(self, uuid, localEsxUtil):
        #print "powerOnVm"
        #localEsxUtilOId = localEsxUtil.objectID
        #if self.haThread is None:
            #return {}
        #myParams = {\
            #'cmd': 'find_entity_views',
            #'admUtilLinuxHa': localEsxUtil,
            #'view_type': 'VirtualMachine',
            #'filter': {'config.uuid':uuid},
        #}
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #self.haThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #esxObjList = self.haThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['out'].task_done()
        #if len(esxObjList) == 0:
            #return None
        #esxObj = esxObjList[0]
        #myParams = {\
            #'admUtilLinuxHa': localEsxUtil,
            #'cmd': 'call_fcnt_on_obj',
            #'perlRef': esxObj['perlRef'],
            #'fnct_name': 'PowerOnVM_Task',
            #'fnct_args': {},
        #}
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #self.haThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #esxObjList = self.haThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['out'].task_done()

    #def shutdownHostEsxHost(self, esxName, localEsxUtil):
        #print "shutdownHostEsxHost"
        #localEsxUtilOId = localEsxUtil.objectID
        #if self.haThread is None:
            #return {}
        #myParams = {\
            #'cmd': 'find_entity_views',
            #'admUtilLinuxHa': localEsxUtil,
            #'view_type': 'HostSystem',
            #'filter': {'name':esxName},
        #}
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #self.haThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #esxObjList = self.haThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['out'].task_done()
        #if len(esxObjList) == 0:
            #return None
        #esxObj = esxObjList[0]
        #myParams = {\
            #'admUtilLinuxHa': localEsxUtil,
            #'cmd': 'call_fcnt_on_obj',
            #'perlRef': esxObj['perlRef'],
            #'fnct_name': 'ShutdownHost_Task',
            #'fnct_args': {'force':1},
        #}
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #self.haThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #esxObjList = self.haThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['out'].task_done()

    #def enterMaintenanceModeEsxHost(self, esxName, localEsxUtil):
        #print "enterMaintenanceModeEsxHost"
        #localEsxUtilOId = localEsxUtil.objectID
        #if self.haThread is None:
            #return {}
        #myParams = {\
            #'cmd': 'find_entity_views',
            #'admUtilLinuxHa': localEsxUtil,
            #'view_type': 'HostSystem',
            #'filter': {'name':esxName},
        #}
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #self.haThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #esxObjList = self.haThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['out'].task_done()
        #if len(esxObjList) == 0:
            #return None
        #esxObj = esxObjList[0]
        #myParams = {\
            #'admUtilLinuxHa': localEsxUtil,
            #'cmd': 'call_fcnt_on_obj',
            #'perlRef': esxObj['perlRef'],
            #'fnct_name': 'EnterMaintenanceMode_Task',
            #'fnct_args': {'timeout': 30},
        #}
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #self.haThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #esxObjList = self.haThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['out'].task_done()

    #def getEsxRoomUuid(self, uuid, localEsxUtil):
        #print "getEsxRoomUuid"
        #localEsxUtilOId = localEsxUtil.objectID
        #if self.haThread is None:
            #return {}
        #myParams = {\
            #'cmd': 'find_entity_views',
            #'admUtilLinuxHa': localEsxUtil,
            #'view_type': 'VirtualMachine',
            #'filter': {'config.uuid':uuid},
        #}
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #self.haThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #esxObjList = self.haThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['out'].task_done()
        #if len(esxObjList) == 0:
            #return None
        #esxObj = esxObjList[0]
        #myParams = {\
            #'admUtilLinuxHa': localEsxUtil,
            #'cmd': 'eval_on_obj',
            #'perlRef': esxObj['perlRef'],
            #'eval_text': 'perl.call(\'Vim::get_view\', mo_ref = obj.runtime().host()).name',
            #'fnct_args': {},
        #}
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #self.haThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['in'].join()
        #esxServerUuid = self.haThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        #self.haThread.getQueue(localEsxUtilOId)['out'].task_done()
        #return esxServerUuid

from zope.app.appsetup import appsetup
try:
    appsetup.getConfigSource().index("site.zcml")
    globalLinuxHaUtility = GlobalLinuxHaUtility()
except ValueError:
    # dont start thread
    pass
    
#@adapter(IAdmUtilLinuxHa, IObjectModifiedEvent)
#def notifyAdmUtilLinuxHaModifiedEvent(instance, event):
    #print "notifyAdmUtilLinuxHaModifiedEvent"
    #if IAdmUtilLinuxHa.providedBy(event.object):
        #event.object.connect2VimServer()
