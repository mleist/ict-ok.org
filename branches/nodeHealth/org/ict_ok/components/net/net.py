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
from org.ict_ok.components.host.special.vmware_esx.interfaces import \
     IHostVMwareEsx

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

    def eventInp_inward_relaying_shutdown(self, eventMsg=None):
        """
        forward the event to all objects in this container through the signal filter
        """
        print "Net.eventInp_inward_relaying_shutdown()"
        for name, obj in self.items():
            # first call
            if INet.providedBy(obj):
                targetFunctionName = "inward_relaying_shutdown"
                logText = u"inward relaying to net '%s'" % obj.ikName
            elif IHostVMwareEsx.providedBy(obj):
                targetFunctionName = "inward_relaying_shutdown"
                logText = u"inward relaying to esx host '%s'" % obj.ikName
            elif IHostVMwareVm.providedBy(obj):
                targetFunctionName = None
            else:
                targetFunctionName = "shutdown"
                logText = u"send shutdown to '%s'" % obj.ikName
            if targetFunctionName is not None:
                if eventMsg is not None:
                    inst_event = MsgEvent(senderObj = self,
                                          oidEventObject = eventMsg.oidEventObject,
                                          logText = logText,
                                          targetFunctionName = targetFunctionName)
                    eventMsg.stopit(self,
                                    u"relaying by site '%s'" % self.ikName)
                else:
                    inst_event = MsgEvent(senderObj = self,
                                          logText = logText,
                                          targetFunctionName = targetFunctionName)
                obj.injectInpEQueue(inst_event)
            # second call
            if IHostVMwareEsx.providedBy(obj):
                targetFunctionName = "shutdown"
                logText = u"send shutdown to esx host '%s'" % obj.ikName
            else:
                targetFunctionName = None
            if targetFunctionName is not None:
                if eventMsg is not None:
                    inst_event = MsgEvent(senderObj = self,
                                          oidEventObject = eventMsg.oidEventObject,
                                          logText = logText,
                                          targetFunctionName = targetFunctionName)
                    eventMsg.stopit(self,
                                    u"relaying by site '%s'" % self.ikName)
                else:
                    inst_event = MsgEvent(senderObj = self,
                                          logText = logText,
                                          targetFunctionName = targetFunctionName)
                obj.injectInpEQueue(inst_event)

    def get_wcnt(self):
        """
        weighted count of accesses
        """
        sum_wcnt = 0
        for host in self.values():
            sum_wcnt += host.get_wcnt()
        return sum_wcnt
    
    def get_health(self):
        """
        output of health, 0-1 (float)
        """
        if len(self.keys()) > 0:
            health = 0.0
            for host in self.values():
                health += host.get_health() * \
                       (float(host.get_wcnt()) / self.get_wcnt())
        else:
            health = None
        return health


def getAllNetworks():
    """ get a list of all Nets
    """
    retList = []
    uidutil = getUtility(IIntIds)
    for (myid, myobj) in uidutil.items():
        if INet.providedBy(myobj.object):
            retList.append(myobj.object)
    return retList
