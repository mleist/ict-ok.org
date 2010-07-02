# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0612,W0142
#
"""implementation of IpNet

IpNet does ....

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.schema.IPy import IP
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.superclass.superclass import MsgEvent
from org.ict_ok.components.ipnet.interfaces import \
    IIpNet, IEventIfEventIpNet, IAddIpNet, IIpNetFolder
from org.ict_ok.components.host.special.vmware_vm.interfaces import \
     IHostVMwareVm
from org.ict_ok.components.host.special.vmware_esx.interfaces import \
     IHostVMwareEsx
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents, \
    ComponentsFromObjList
from org.ict_ok.components.ip_address.interfaces import IIpAddress

def AllIpNetTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IIpNet, 'ipv4')

def AllIpNets(dummy_context):
    return AllComponents(dummy_context, IIpNet,
                         True, 'ipv4')

def AllUnusedOrSelfIpNets(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IIpNet,
                                     'parentnet', 'ipv4')

def AllValidSubIpNets(dummy_context):
    uidutil = getUtility(IIntIds)
    validObjects = []
    if IIpNet.providedBy(dummy_context):
        myIpNetIp = IP(dummy_context.ipv4)
        for (oid, oobj) in uidutil.items():
            if IIpNet.providedBy(oobj.object):
                i_IpNetIp = IP(oobj.object.ipv4)
                if i_IpNetIp in myIpNetIp and \
                    oobj.object != dummy_context:
                    validObjects.append(oobj.object)
    else:
        for (oid, oobj) in uidutil.items():
            if IIpNet.providedBy(oobj.object):
                validObjects.append(oobj.object)
    return ComponentsFromObjList(dummy_context, validObjects, 'ipv4')


IpNet_IpNets_RelManager = \
       FieldRelationManager(IIpNet['subnets'],
                            IIpNet['parentnet'],
                            relType='parentnet:subnets')

IpNet_IpAddresses_RelManager = \
       FieldRelationManager(IIpNet['ipAddresses'],
                            IIpAddress['ipNet'],
                            relType='ipNet:ipAddresses')


class IpNet(Component):
    """
    the template instance
    """

    implements(IIpNet, IEventIfEventIpNet)
    shortName = "ipnet"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    ipv4 = FieldProperty(IIpNet['ipv4'])

    subnets = RelationPropertyOut(IpNet_IpNets_RelManager)
    parentnet = RelationPropertyIn(IpNet_IpNets_RelManager)
    ipAddresses = RelationPropertyOut(IpNet_IpAddresses_RelManager)
    
    eventInpObjs_inward_relaying_shutdown = FieldProperty(\
        IEventIfEventIpNet['eventInpObjs_inward_relaying_shutdown'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(IpNet)
        for (name, value) in data.items():
            if name in IIpNet.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.eventInpObjs_inward_relaying_shutdown = set([])
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(IpNet)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)

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
        print "IpNet.eventInp_inward_relaying_shutdown()"
        for name, obj in self.items():
            # first call
            if IIpNet.providedBy(obj):
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
                if host.get_health() is not None:
                    health += host.get_health() * \
                           (float(host.get_wcnt()) / self.get_wcnt())
        else:
            health = None
        return health


class IpNetFolder(ComponentFolder):
    implements(IIpNetFolder, 
               IAddIpNet)
    contentFactory = IpNet
    shortName = "net folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)


class SoapTest:
    def __init__(self, context, request):
        self.context = context
        self.request = request
    def echoString(self, value):
        return value
