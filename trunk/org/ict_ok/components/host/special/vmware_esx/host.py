# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of host object

host object represents a VMware ESX Server
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.catalog.interfaces import ICatalog

# ict_ok.org imports
from org.ict_ok.components.superclass.superclass import MsgEvent
from org.ict_ok.components.host.special.vmware_esx.interfaces import \
     IHostVMwareEsx, IEventIfHostVMwareEsx
from org.ict_ok.components.host.host import Host as HostBase
from org.ict_ok.admin_utils.esx_vim.interfaces import IAdmUtilEsxVim


class Host(HostBase):
    """
    the VmWare host instance
    """
    implements(IHostVMwareEsx, IEventIfHostVMwareEsx)

    esxUuid = FieldProperty(IHostVMwareEsx['esxUuid'])
    eventInpObjs_inward_relaying_shutdown = FieldProperty(\
        IEventIfHostVMwareEsx['eventInpObjs_inward_relaying_shutdown'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        HostBase.__init__(self, **data)
        for (name, value) in data.items():
            if name in IHostVMwareEsx.names():
                setattr(self, name, value)
        self.eventInpObjs_inward_relaying_shutdown = set([])
        self.ikRevision = __version__

    def eventInp_inward_relaying_shutdown(self, eventMsg=None):
        """
        forward the event to all objects in this container through the signal filter
        """
        print "HostVMwareEsx.eventInp_inward_relaying_shutdown()"
        if self.inEventMask(eventMsg):
            print "Filter **match**"
        else:
            print "Filter ** doesn't match**"
        esx_utility = zapi.getUtility(IAdmUtilEsxVim)
        if esx_utility and len(self.esxUuid) > 0:
            self.appendHistoryEntry("inward relaying shutdown")
            #esx_utility.getFilteredList(self.esxUuid)
            myParams = {\
                'cmd': 'find_entity_views',
                'view_type': 'HostSystem',
                'admUtilEsxVim': esx_utility,
                'filter': {'name':self.esxUuid},
                }
            myEsxDict = esx_utility.get_EsxVimObject_Dict(myParams, None)
            if not myEsxDict.has_key(self.esxUuid):
                print "dont find"
                return None
            myEsxObj = myEsxDict[self.esxUuid]
            myParams = {\
                'cmd': 'find_entity_views',
                'view_type': 'VirtualMachine',
                'admUtilEsxVim': esx_utility,
                'begin_entity': myEsxObj.perlEsxObjRef,
                'filter': {'runtime.powerState':'poweredOn'},
                }
            myVmDict = esx_utility.get_EsxVimObject_Dict(myParams, None)
            my_catalog = zapi.getUtility(ICatalog)
            for vmName, vmObj in myVmDict.items():
                print "----->", vmObj.uuid
                res = my_catalog.searchResults(host_vmuuid_index=str(vmObj.uuid))
                #import pdb
                #pdb.set_trace()
                if len(res) > 0:
                    internalVmObj = list(res)[0]
                    print "ref-->", internalVmObj
                    inst_event = MsgEvent(senderObj = self,
                                          oidEventObject = eventMsg.oidEventObject,
                                          logText = u"inward relaying by esx host '%s'"\
                                          % self.ikName,
                                          targetFunctionName = 'shutdown')
                    internalVmObj.injectInpEQueue(inst_event)
            

    def eventInp_shutdown(self, eventMsg=None):
        """ start the shutdown of the host """
        print "HostVMwareEsx.eventInp_shutdown()"
        #eventProcessed = False
        #if self.inEventMask(eventMsg):
            #eventProcessed = True
            #eventMsg.stopit(self, "Host.eventInp_shutdown")
            #utilXbar = queryUtility(IAdmUtilEventCrossbar)
            #utilEvent = utilXbar[eventMsg.oidEventObject]
            #if utilEvent.dryRun:
                #msgText = u"Shutdown (dry run)"
                #print "Host.eventInp_shutdown (%s) (dry run)             ############## <-" % (self.ikName)
            #else:
                #msgText = u"Shutdown"
                #print "Host.eventInp_shutdown (%s)              ############## <-" % (self.ikName)
                #self.poweroff()
                #self.appendHistoryEntry(msgText)
        #return eventProcessed
