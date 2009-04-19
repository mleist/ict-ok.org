# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Interface

Interface does ....

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.folder import Folder

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.component import Component
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.interface.interfaces import \
    IInterface, IAddInterface, IInterfaceFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
#from org.ict_ok.components.host.host import Host_Interfaces_RelManager
from org.ict_ok.components.device.device import Device_Interface_RelManager
#from org.ict_ok.components.physical_connector.physical_connector import \
#    PhysicalConnector_Interface_RelManager
from org.ict_ok.components.physical_connector.interfaces import \
    IPhysicalConnector#, IPhysicalConnectorFolder, IAddPhysicalConnector
from org.ict_ok.components.physical_link.interfaces import IPhysicalLink
from org.ict_ok.components.physical_link.physical_link import \
    PhysicalLinks_PhysicalConnectors_RelManager
from org.ict_ok.osi import osi
from org.ict_ok.components.physical_component.physical_component import \
    PhysicalComponent
from org.ict_ok.components.ip_address.interfaces import IIpAddress

def AllInterfaceTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IInterface)

def AllInterfaces(dummy_context):
    return AllComponents(dummy_context, IInterface,
                         additionalAttrNames=['device'])

def AllUnusedOrUsedDeviceInterfaces(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IInterface, 'device',
                                     additionalAttrNames=['device'])

def AllUnusedOrUsedPhysicalConnectorInterfaces(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IInterface, 'physicalConnector',
                                     additionalAttrNames=['device'])


Interface_IpAddresses_RelManager = \
       FieldRelationManager(IInterface['ipAddresses'],
                            IIpAddress['interface'],
                            relType='interface:ipAddresses')


class Interface(PhysicalComponent):
    """
    the template instance
    """

    implements(IInterface)
    shortName = "interface"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    netType = FieldProperty(IInterface['netType'])
    mac = FieldProperty(IInterface['mac'])
    ipv4List = FieldProperty(IInterface['ipv4List'])
    
    device = RelationPropertyIn(Device_Interface_RelManager)
    #host2 = RelationPropertyIn(Host_Interfaces_RelManager)
    connectorPinout = FieldProperty(IPhysicalConnector['connectorPinout'])
    links = RelationPropertyIn(PhysicalLinks_PhysicalConnectors_RelManager)

#    physicalConnector = RelationPropertyOut(PhysicalConnector_Interface_RelManager)
    ipAddresses = RelationPropertyOut(Interface_IpAddresses_RelManager)

    fullTextSearchFields = ['netType', 'mac',
                            'ipv4List']
    fullTextSearchFields.extend(PhysicalComponent.fullTextSearchFields)
    
    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalComponent.__init__(self, **data)
        ipv4List = []
        refAttributeNames = getRefAttributeNames(Interface)
        for (name, value) in data.items():
            if name in IInterface.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__
        
    def store_refs(self, **data):
        PhysicalComponent.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(Interface)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)

    def getAllPhysicalConnectors(self, connectorSet, maxDepth=10):
        if maxDepth < 0:
            raise Exception
        for link in self.links:
            if IPhysicalLink.providedBy(link):
                link.getAllPhysicalConnectors(connectorSet, maxDepth-1)


class InterfaceFolder(Superclass, Folder):
    implements(IInterfaceFolder, 
               IImportCsvData,
               IImportXlsData,
               IAddInterface)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
