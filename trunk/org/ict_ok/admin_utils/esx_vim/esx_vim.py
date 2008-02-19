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
"""implementation of a "esx_vim daemon" 
"""

__version__ = "$Id$"

# phython imports
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
from org.ict_ok.admin_utils.esx_vim.interfaces import IAdmUtilEsxVim
from org.ict_ok.admin_utils.esx_vim.interfaces import IGlobalEsxVimUtility
from org.ict_ok.admin_utils.esx_vim.esx_vim_connection import \
     EsxVimConnectionThread
from zope.app.container.contained import contained

logger = logging.getLogger("AdmUtilEsxVim")
_ = MessageFactory('org.ict_ok')

from zope.annotation.interfaces import IAnnotations

class AdmUtilEsxVim(Supernode):
    """Implementation of local EsxVim Utility"""

    implements(IAdmUtilEsxVim, IReadContainer, IAnnotations)

    esxVimServerActive = FieldProperty(IAdmUtilEsxVim['esxVimServerActive'])
    esxVimServerIp = FieldProperty(IAdmUtilEsxVim['esxVimServerIp'])
    esxVimServerPort = FieldProperty(IAdmUtilEsxVim['esxVimServerPort'])
    esxVimUsername = FieldProperty(IAdmUtilEsxVim['esxVimUsername'])
    esxVimPassword = FieldProperty(IAdmUtilEsxVim['esxVimPassword'])

    lastEsxVim = "no signal since start"

    def __init__(self):
        print "AdmUtilEsxVim.__init__"
        Supernode.__init__(self)
        self.connStatus = u"never connected"
        self.apiFullName = u"never get API"
        self.ikRevision = __version__

    def connect2VimServer(self):
        print "AdmUtilEsxVim.connect2VimServer: ", self.getObjectId()
        globalEsxVimUtility.connectToEsxVim(self)

    def setConnStatus(self, connString):
        if self.connStatus != connString:
            self.connStatus = connString
            #self._p_changed = True

    def __getitem__(self, key):
        '''See interface `IReadContainer`'''
        #print "AdmUtilEsxVim.__getitem__(%s)" % (key)
        if self.has_key(key):
            return self[key]
        myDict = globalEsxVimUtility.get_EsxVimAllDict(self, self)
        if myDict.has_key(key):
            return myDict[key]
        raise KeyError
    
    def __getattr__(self, key):
        #print "AdmUtilEsxVim.__getattr__(%s)" % (key)
        if self.has_key(key):
            return self[key]
        myDict = globalEsxVimUtility.get_EsxVimAllDict(self, self)
        if myDict.has_key(key):
            return myDict[key]
        if key == '__annotations__':
            return None
        if key == '__getnewargs__':
            return None
        raise KeyError
    
    def powerOffVm(self, uuid):
        return globalEsxVimUtility.powerOffVm(uuid, self)
 
    def powerOnVm(self, uuid):
        return globalEsxVimUtility.powerOnVm(uuid, self)

    def getEsxRoomUuid(self, uuid):
        return globalEsxVimUtility.getEsxRoomUuid(uuid, self)
 
    def values(self):
        '''See interface `IReadContainer`'''
        print "AdmUtilEsxVim.values"
        #return globalEsxVimUtility.get_EsxVimDatacenter_values(self)
        #return globalEsxVimUtility.get_EsxVimDatacenter_Dict(self, self).values()
        return globalEsxVimUtility.get_EsxVimAllDict(self, self).values()
        #return getTestDict(self).values()

    def receiveEsxVim(self, request, str_time, mode=None):
        """receive esx_vim signal
        """
        #logger.info(u"AdmUtilEsxVim::receiveEsxVim(%s, %s) in '%s'" \
                    #% (str_time, mode,zapi.getPath(self)))
        self.lastEsxVim = str_time
        dcore = IWriteZopeDublinCore(self)
        dcore.modified = datetime.utcnow()

    def getEsxVimTime(self):
        """get last esx_vim timestamp
        """
        try:
            retVal = self.lastEsxVim
        except NameError:
            self.__setattr__("lastEsxVim", "not set")
            retVal = self.lastEsxVim
        return retVal


class GlobalEsxVimUtility(object):

    implements(IGlobalEsxVimUtility)

    lastEsxVim = "no signal since start"

    def __init__(self):
        logger.info(u"GlobalEsxVimUtility started")
        super(GlobalEsxVimUtility, self).__init__(self)
        self.subscriber_list = []
        self.connection_dict = {}
        #self.esxThread = None
        self.esxThread = EsxVimConnectionThread()
        self.esxThread.globalEsxVim = self
        self.esxThread.setDaemon(0)
        self.esxThread.start()
        self.timeStarted = datetime.utcnow()
        self.ikRevision = __version__

    def getUtilityVersion(self):
        """ global und svn Version of Utility """
        return "ddd - ", GlobalEsxVimUtility.lastEsxVim, " - ", \
               "Ver0.1"," - ", self.ikRevision, " - eee"

    def getUptime(self):
        """uptime of Utility"""
        return datetime.utcnow() - self.timeStarted

    def subscribeToEsxVim(self, obj):
        #logger.info(u"GlobalEsxVimUtility::subscribe2esx_vim(%s)" % obj)
        if obj not in self.subscriber_list:
            self.subscriber_list.append(obj)
            #self.connection_dict[obj.getObjectId()] = None

    def unsubscribeFromEsxVim(self, obj):
        #logger.info(u"GlobalEsxVimUtility::unsubscribeFromEsxVim(%s)" % obj)
        if obj in self.subscriber_list:
            self.subscriber_list.remove(obj)
            #del self.connection_dict[obj.getObjectId()]

    def connectToEsxVim(self, obj):
        logger.info(u"GlobalEsxVimUtility::connectToEsxVim(%s)" % obj)
        if obj.esxVimServerActive:
            connection = {}
            connection['con'] = None
            connection['ip'] = obj.esxVimServerIp
            connection['port'] = obj.esxVimServerPort
            connection['username'] = obj.esxVimUsername
            connection['password'] = obj.esxVimPassword
            print "connection: %s" % (connection)
            if not connection['con']:
                print "make con"
                if not self.esxThread:
                    self.esxThread = EsxVimConnectionThread()
                    self.esxThread.globalEsxVim = self
                    self.esxThread.createQueue(obj.getObjectId())
#                    self.esxThread.localEsxVim = obj
                    self.esxThread.setDaemon(0)
                    self.esxThread.start()
                else:
                    print "esxThread already active?"
                #perl.require("VMware::VIM2Runtime")
                #perl.require("VMware::VILib")
                #perl.call("Vim::login",
                          #service_url = "https://192.168.154.10:443/sdk/webService",
                          #user_name="ikom.trol",
                          #password="ikom.trol")
            else:
                print "check con if already up"

    def get_EsxVimDatacenter_keys(self, localEsxUtil):
        print "IkGlobalEsxVimUtility.get_EsxVimDatacenter_keys(%s,%s)" % \
              (self, localEsxUtil)
        return []

    def get_EsxVimDatacenter_getitem(self, localEsxUtil, key):
        print "IkGlobalEsxVimUtility.get_EsxVimDatacenter_getitem(%s,%s,%s)" % \
              (self, localEsxUtil, key)
        return None

    def get_EsxVimDatacenter_values(self, localEsxUtil):
        print "IkGlobalEsxVimUtility.get_EsxVimDatacenter_values(%s,%s)" % \
              (self, localEsxUtil)
        return []

    def get_EsxVimAllDict(self, localEsxUtil, parentObj):
        retDict = {}
        
        objFolder = createObject(\
            "org.ict_ok.admin_utils.esx_vim.esx_vim_folder.EsxVimFolder")
        objFolder.localEsxUtil = localEsxUtil
        objFolder.name = u'Datacenters'
        objFolder.esxObjectTypes = r'Datacenter'
        contained(objFolder, parentObj, u'Datacenters')
        objFolder.__parent__ = parentObj
        retDict[u"Datacenters"] = objFolder

        objFolder = createObject(\
            "org.ict_ok.admin_utils.esx_vim.esx_vim_folder.EsxVimFolder")
        objFolder.localEsxUtil = localEsxUtil
        objFolder.name = u'HostSystems'
        objFolder.esxObjectTypes = r'HostSystem'
        contained(objFolder, parentObj, u'HostSystems')
        objFolder.__parent__ = parentObj
        retDict[u'HostSystems'] = objFolder
        
        objFolder = createObject(\
            "org.ict_ok.admin_utils.esx_vim.esx_vim_folder.EsxVimFolder")
        objFolder.localEsxUtil = localEsxUtil
        objFolder.name = u'VirtualMachines'
        objFolder.esxObjectTypes = r'VirtualMachine'
        contained(objFolder, parentObj, u'VirtualMachines')
        objFolder.__parent__ = parentObj
        retDict[u'VirtualMachines'] = objFolder
        
        objFolder = createObject(\
            "org.ict_ok.admin_utils.esx_vim.esx_vim_folder.EsxVimFolder")
        objFolder.localEsxUtil = localEsxUtil
        objFolder.name = u'Folder'
        objFolder.esxObjectTypes = r'Folder'
        contained(objFolder, parentObj, u'Folder')
        objFolder.__parent__ = parentObj
        retDict[u'Folder'] = objFolder
        return retDict
        

    def get_EsxVimObject_Dict(self, myParams, parentObj):
        """ TODO: caching here please
        """
        print "get_EsxVimDatacenter_Dict"
        if self.esxThread is None:
            return {}
        localEsxUtil = myParams['admUtilEsxVim']
        utilOId = localEsxUtil.getObjectId()
        #print "aa12"
        #myParams = {\
            #'cmd': 'find_entity_views',
            #'view_type': 'Datacenter',
            #'admUtilEsxVim': localEsxUtil,
            #}
        self.esxThread.getQueue(utilOId)['in'].put(myParams, True, 15)
        #print "aa13:", utilOId
        self.esxThread.getQueue(utilOId)['in'].join()
        #print "aa14"
        #self.esxThread.queue1_in.put(localEsxUtil, True, 5)
        #self.esxThread.queue1_in.join()
        esxObjList = self.esxThread.getQueue(utilOId)['out'].get(True, 15)
        #print "esxObjList: ", esxObjList
        #print "aa15"
        self.esxThread.getQueue(utilOId)['out'].task_done()
        #print "aa16"
        retDict = {}
        for esxObj in esxObjList:
            #print "datacenter0123:", datacenter
            newObj = None
            if esxObj['esxType'] == 'Datacenter':
                newObj = createObject(\
                    "org.ict_ok.admin_utils.esx_vim.esx_vim_datacenter.EsxVimDatacenter")
            elif esxObj['esxType'] == 'HostSystem':
                newObj = createObject(\
                    "org.ict_ok.admin_utils.esx_vim.esx_vim_hostsystem.EsxVimHostSystem")
            elif esxObj['esxType'] == 'VirtualMachine':
                newObj = createObject(\
                    "org.ict_ok.admin_utils.esx_vim.esx_vim_virtual_machine.EsxVimVirtualMachine")
            elif esxObj['esxType'] == 'Folder':
                newObj = createObject(\
                    "org.ict_ok.admin_utils.esx_vim.esx_vim_folder.EsxVimFolder")
            if newObj:
                contained(newObj, parentObj, esxObj['name'])
                newObj.localEsxUtil = localEsxUtil
                newObj.overallStatus = esxObj['overallStatus']
                newObj.name = esxObj['name']
                if esxObj.has_key('perlRef'):
                    newObj.perlEsxObjRef = esxObj['perlRef']
                newObj.__parent__ = parentObj
                retDict[esxObj['name']] = newObj
        return retDict

    def powerOffVm(self, uuid, localEsxUtil):
        print "powerOffVm"
        localEsxUtilOId = localEsxUtil.objectID
        if self.esxThread is None:
            return {}
        myParams = {\
            'cmd': 'find_entity_views',
            'admUtilEsxVim': localEsxUtil,
            'view_type': 'VirtualMachine',
            'filter': {'config.uuid':uuid},
            }
        self.esxThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        self.esxThread.getQueue(localEsxUtilOId)['in'].join()
        if self.esxThread.getQueue(localEsxUtilOId)['out'].qsize() > 0:
            esxObjList = self.esxThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
            self.esxThread.getQueue(localEsxUtilOId)['out'].task_done()
            esxObj = esxObjList[0]
            myParams = {\
                'admUtilEsxVim': localEsxUtil,
                'cmd': 'call_fcnt_on_obj',
                'perlRef': esxObj['perlRef'],
                'fnct_name': 'ShutdownGuest',
                'fnct_args': [],
                }
            self.esxThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
            self.esxThread.getQueue(localEsxUtilOId)['in'].join()
            if self.esxThread.getQueue(localEsxUtilOId)['out'].qsize() > 0:
                esxObjList = self.esxThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
                self.esxThread.getQueue(localEsxUtilOId)['out'].task_done()

 
    def powerOnVm(self, uuid, localEsxUtil):
        print "powerOnVm"
        localEsxUtilOId = localEsxUtil.objectID
        if self.esxThread is None:
            return {}
        myParams = {\
            'cmd': 'find_entity_views',
            'admUtilEsxVim': localEsxUtil,
            'view_type': 'VirtualMachine',
            'filter': {'config.uuid':uuid},
            }
        self.esxThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        self.esxThread.getQueue(localEsxUtilOId)['in'].join()
        esxObjList = self.esxThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        self.esxThread.getQueue(localEsxUtilOId)['out'].task_done()
        esxObj = esxObjList[0]
        myParams = {\
            'admUtilEsxVim': localEsxUtil,
            'cmd': 'call_fcnt_on_obj',
            'perlRef': esxObj['perlRef'],
            'fnct_name': 'PowerOnVM_Task',
            'fnct_args': [],
            }
        self.esxThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        self.esxThread.getQueue(localEsxUtilOId)['in'].join()
        esxObjList = self.esxThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        self.esxThread.getQueue(localEsxUtilOId)['out'].task_done()

    def getEsxRoomUuid(self, uuid, localEsxUtil):
        print "getEsxRoomUuid"
        localEsxUtilOId = localEsxUtil.objectID
        if self.esxThread is None:
            return {}
        myParams = {\
            'cmd': 'find_entity_views',
            'admUtilEsxVim': localEsxUtil,
            'view_type': 'VirtualMachine',
            'filter': {'config.uuid':uuid},
            }
        self.esxThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        self.esxThread.getQueue(localEsxUtilOId)['in'].join()
        esxObjList = self.esxThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        self.esxThread.getQueue(localEsxUtilOId)['out'].task_done()
        esxObj = esxObjList[0]
        myParams = {\
            'admUtilEsxVim': localEsxUtil,
            'cmd': 'eval_on_obj',
            'perlRef': esxObj['perlRef'],
            'eval_text': 'perl.call(\'Vim::get_view\', mo_ref = obj.runtime().host()).name',
            'fnct_args': [],
            }
        self.esxThread.getQueue(localEsxUtilOId)['in'].put(myParams, True, 15)
        self.esxThread.getQueue(localEsxUtilOId)['in'].join()
        esxServerUuid = self.esxThread.getQueue(localEsxUtilOId)['out'].get(True, 15)
        self.esxThread.getQueue(localEsxUtilOId)['out'].task_done()
	return esxServerUuid


globalEsxVimUtility = GlobalEsxVimUtility()

@adapter(IAdmUtilEsxVim, IObjectModifiedEvent)
def notifyAdmUtilEsxVimModifiedEvent(instance, event):
    print "notifyAdmUtilEsxVimModifiedEvent"
    if IAdmUtilEsxVim.providedBy(event.object):
        event.object.connect2VimServer()
