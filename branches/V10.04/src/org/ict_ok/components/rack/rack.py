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
"""implementation of Rack"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.rack.interfaces import \
    IAddRack, IRack, IRackFolder
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.patchpanel.interfaces import IPatchPanel
from org.ict_ok.components.switch.interfaces import ISwitch
from org.ict_ok.components.physical_component.physical_component import \
    PhysicalComponent

def AllRackTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IRack)

def AllRacks(dummy_context):
    return AllComponents(dummy_context, IRack)

def AllUnusedOrUsedRoomRacks(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IRack, 'room')


Rack_PatchPanels_RelManager = \
       FieldRelationManager(IRack['patchpanels'],
                            IPatchPanel['rack'],
                            relType='rack:patchpanels')

Rack_Switches_RelManager = \
       FieldRelationManager(IRack['patchpanels'],
                            ISwitch['rack'],
                            relType='rack:switches')


class Rack(PhysicalComponent):
    """
    the template instance
    """
    implements(IRack)
    shortName = "rack"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    height = FieldProperty(IRack['height'])
    patchpanels = RelationPropertyOut(Rack_PatchPanels_RelManager)
    switches = RelationPropertyOut(Rack_Switches_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(PhysicalComponent.fullTextSearchFields)
        

    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalComponent.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Rack)
        for (name, value) in data.items():
            if name in IRack.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Rack)

    def store_refs(self, **data):
        PhysicalComponent.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class RackFolder(ComponentFolder):
    implements(IRackFolder,
               IAddRack)
    contentFactory = Rack
    shortName = "rack folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
