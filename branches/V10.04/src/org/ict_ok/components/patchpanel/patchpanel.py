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
"""implementation of PatchPanel"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.patchpanel.interfaces import \
    IAddPatchPanel, IPatchPanel, IPatchPanelFolder
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.rack.rack import Rack_PatchPanels_RelManager
from org.ict_ok.components.patchport.interfaces import IPatchPort
from org.ict_ok.components.physical_component.physical_component import \
    PhysicalComponent

def AllPatchPanelTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IPatchPanel)

def AllPatchPanels(dummy_context):
    return AllComponents(dummy_context, IPatchPanel)

def AllUnusedOrUsedRackPatchPanels(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IPatchPanel, 'rack')


PatchPanel_PatchPorts_RelManager = \
       FieldRelationManager(IPatchPanel['patchports'],
                            IPatchPort['patchpanel'],
                            relType='patchpanel:patchports')




class PatchPanel(PhysicalComponent):
    """
    the template instance
    """
    implements(IPatchPanel)
    shortName = "patchpanel"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    portCount = FieldProperty(IPatchPanel['portCount'])
    rack = RelationPropertyIn(Rack_PatchPanels_RelManager)
    patchports = RelationPropertyOut(PatchPanel_PatchPorts_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(PhysicalComponent.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalComponent.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(PatchPanel)
        for (name, value) in data.items():
            if name in IPatchPanel.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(PatchPanel)

    def store_refs(self, **data):
        PhysicalComponent.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class PatchPanelFolder(ComponentFolder):
    implements(IPatchPanelFolder,
               IAddPatchPanel)
    contentFactory = PatchPanel
    shortName = "patchpanel folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
