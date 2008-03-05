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
"""implementation of Net

Net does ....

"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

# ict_ok.org imports
from org.ict_ok.schema.IPy import IP
from org.ict_ok.components.component import Component
from org.ict_ok.components.superclass.superclass import MsgEvent
from org.ict_ok.components.net.interfaces import INet, IEventIfEventNet
from org.ict_ok.components.host.special.vmware_vm.interfaces import \
     IHostVMwareVm

class Net(Component):
    """
    the template instance
    """

    implements(INet, IEventIfEventNet)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    ipv4 = FieldProperty(INet['ipv4'])

    eventInpObjs_inward_relaying_shutdown = FieldProperty(\
        IEventIfEventNet['eventInpObjs_inward_relaying_shutdown'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        for (name, value) in data.items():
            if name in INet.names():
                setattr(self, name, value)
        self.eventInpObjs_inward_relaying_shutdown = set([])
        self.ikRevision = __version__

    def containsIp(self, ipString):
        """ is ip(String) part of this network?
        """
        myIp = IP(self.ipv4)
        testIp = IP(ipString)
        return testIp in myIp

    #def eventInp_inward_relaying_shutdown(self, eventMsg=None):
        #"""
        #forward the event to all objects in this container through the signal filter
        #"""
        ##eventMsg.stopit(self, "Net.eventInp_inward_relaying_shutdown")
        ##print "Net.eventInp_inward_relaying_shutdown (%s)       " \
        ##"       ############## <-" % (self.ikName)
        #hostsProcessed = []
        #for name, obj in self.items():
            ##print "-> ", obj
            #try:
                #if obj.eventInp_shutdown(eventMsg):
                    #hostsProcessed.append(obj.ikName)
            #except AttributeError:
                #print "Dont find method"
        #if len(hostsProcessed) > 0:
            #eventMsg.stopit(self, "Net.inward_relaying_shutdown "\
                            #"processed @ %s" % " ,".join(hostsProcessed))
            ##for attrName in obj.__dict__:
                ##print "attr:   %s" % (attrName)
                ##if attrName.find("eventInp_shutdown") == 0: # attribute name starts with ...
                    ##fnct = getattr(obj, "eventInp_shutdown", None)
                    ##if fnct is not None:
                        ##fnct(eventMsg)

    def eventInp_inward_relaying_shutdown(self, eventMsg=None):
        """
        forward the event to all objects in this container through the signal filter
        """
        print "Net.eventInp_inward_relaying_shutdown()"
        for name, obj in self.items():
            if INet.providedBy(obj):
                targetFunctionName = "inward_relaying_shutdown"
            elif IHostVMwareVm.providedBy(obj):
                targetFunctionName = None
            else:
                targetFunctionName = "shutdown"
            if targetFunctionName is not None:
                if eventMsg is not None:
                    inst_event = MsgEvent(senderObj = self,
                                          oidEventObject = eventMsg.oidEventObject,
                                          logText = u"inward relaying by net '%s'"\
                                          % self.ikName,
                                          targetFunctionName = targetFunctionName)
                    eventMsg.stopit(self,
                                    u"relaying by site '%s'" % self.ikName)
                else:
                    inst_event = MsgEvent(senderObj = self,
                                          logText = u"inward relaying by net '%s'"\
                                          % self.ikName,
                                          targetFunctionName = targetFunctionName)
                obj.injectInpEQueue(inst_event)


def getAllNetworks():
    """ get a list of all Nets
    """
    retList = []
    uidutil = getUtility(IIntIds)
    for (myid, myobj) in uidutil.items():
        if INet.providedBy(myobj.object):
            retList.append(myobj.object)
    return retList
