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
"""implementation of LogicalComponent"""

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
from org.ict_ok.components.logical_component.interfaces import \
    ILogicalComponent, ILogicalComponentFolder, IAddLogicalComponent
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import Component
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.room.room import Room_LogicalComponents_RelManager

def AllLogicalComponentTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, ILogicalComponent)

def AllLogicalComponents(dummy_context):
    return AllComponents(dummy_context, ILogicalComponent)

def AllUnusedOrUsedRoomLogicalComponents(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, ILogicalComponent, 'room')

def AllUnusedOrUsedInterfaceLogicalComponents(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, ILogicalComponent, 'interface')

LogicalComponent_Interface_RelManager = \
    FieldRelationManager(ILogicalComponent['interface'],
                         IInterface['physicalConnector'],
                         relType='physicalConnector:interface')


class LogicalComponent(Component):
    """
    the template instance
    """
    implements(ILogicalComponent)
    shortName = "logical_component"
    
    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(LogicalComponent)
        for (name, value) in data.items():
            if name in ILogicalComponent.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        refAttributeNames = getRefAttributeNames(LogicalComponent)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)
