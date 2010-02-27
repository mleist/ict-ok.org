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
"""implementation of Building

Building does ....

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import getUtility
from zope.schema.fieldproperty import FieldProperty
from zope.app.folder import Folder

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.interfaces import \
    IComponentFolder, IImportCsvData, IImportXlsData
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.building.interfaces import \
    IBuilding, IAddBuilding, IBuildingFolder
from org.ict_ok.components.room.interfaces import IRoom
from org.ict_ok.components.location.location import Location_Buildings_RelManager
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents




def AllBuildingTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IBuilding)

def AllBuildings(dummy_context):
    return AllComponents(dummy_context, IBuilding)

def AllUnusedOrSelfBuildings(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IBuilding, 'location')


Building_Rooms_RelManager = FieldRelationManager(IBuilding['rooms'],
                                                 IRoom['building'],
                                                 relType='building:rooms')


class Building(Component):
    """
    the template instance
    """

    implements(IBuilding)
    shortName = "building"
    containerIface = IBuildingFolder
    # for ..Contained we have to:
    __name__ = __parent__ = None
    #ikAttr = FieldProperty(IBuilding['ikAttr'])
    coordinates = FieldProperty(IBuilding['coordinates'])
    gmapsurl = FieldProperty(IBuilding['gmapsurl'])
    gmapcode = FieldProperty(IBuilding['gmapcode'])

    location = RelationPropertyIn(Location_Buildings_RelManager)
    rooms = RelationPropertyOut(Building_Rooms_RelManager)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Building)
        for (name, value) in data.items():
            if name in IBuilding.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Building)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class BuildingFolder(ComponentFolder):
    implements(IBuildingFolder,
               IAddBuilding)
    contentFactory = Building

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
