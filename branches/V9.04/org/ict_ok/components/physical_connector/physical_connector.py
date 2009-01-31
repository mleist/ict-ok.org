# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of PhysicalConnector"""

__version__ = "$Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $"

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
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.physical_connector.interfaces import \
    IPhysicalConnector, IPhysicalConnectorFolder, IAddPhysicalConnector
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import Component
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.room.room import Room_PhysicalConnectors_RelManager

def AllPhysicalConnectorTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IPhysicalConnector)

def AllPhysicalConnectors(dummy_context):
    return AllComponents(dummy_context, IPhysicalConnector)

def AllUnusedOrUsedRoomPhysicalConnectors(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IPhysicalConnector, 'room')



class PhysicalConnector(Component):
    """
    the template instance
    """
    implements(IPhysicalConnector)
    shortName = "physical_connector"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    
    connectorPinout = FieldProperty(IPhysicalConnector['connectorPinout'])
    
    room = RelationPropertyIn(Room_PhysicalConnectors_RelManager)

    fullTextSearchFields = ['connectorPinout']
    fullTextSearchFields.extend(Component.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(PhysicalConnector)
        for (name, value) in data.items():
            if name in IPhysicalConnector.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        refAttributeNames = getRefAttributeNames(PhysicalConnector)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class PhysicalConnectorFolder(Superclass, Folder):
    implements(IPhysicalConnectorFolder, 
               IImportCsvData,
               IImportXlsData,
               IAddPhysicalConnector)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
