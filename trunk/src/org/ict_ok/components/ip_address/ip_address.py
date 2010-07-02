# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of IpAddress"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports
from lovely.relation.property import RelationPropertyIn

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.ip_address.interfaces import IIpAddress
from org.ict_ok.components.ip_address.interfaces import IIpAddressFolder
from org.ict_ok.components.ip_address.interfaces import IAddIpAddress
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.logical_component.logical_component import \
    LogicalComponent
from org.ict_ok.components.interface.interface import Interface_IpAddresses_RelManager
from org.ict_ok.components.ipnet.ipnet import IpNet_IpAddresses_RelManager

def AllIpAddressTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IIpAddress)

def AllIpAddresses(dummy_context):
    return AllComponents(dummy_context, IIpAddress,
                         True, 'ipv4')
def AllUnusedOrUsedInterfaceIpAddresses(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IIpAddress, 'interface',
                                     'ipv4')
def AllUnusedOrUsedIpNetIpAddresses(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IIpAddress, 'ipNet',
                                     'ipv4')


class IpAddress(LogicalComponent):
    """
    the template instance
    """
    implements(IIpAddress)
    shortName = "ip_address"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    ipv4 = FieldProperty(IIpAddress['ipv4'])
    hostname = FieldProperty(IIpAddress['hostname'])
    interface = RelationPropertyIn(Interface_IpAddresses_RelManager)
    ipNet = RelationPropertyIn(IpNet_IpAddresses_RelManager)

    fullTextSearchFields = ['hostname']
    fullTextSearchFields.extend(LogicalComponent.fullTextSearchFields)
        

    def __init__(self, **data):
        """
        constructor of the object
        """
        LogicalComponent.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(IpAddress)
        for (name, value) in data.items():
            if name in IIpAddress.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(IpAddress)

    def store_refs(self, **data):
        LogicalComponent.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class IpAddressFolder(ComponentFolder):
    implements(IIpAddressFolder,
               IAddIpAddress)
    contentFactory = IpAddress
    shortName = "ip_address folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
