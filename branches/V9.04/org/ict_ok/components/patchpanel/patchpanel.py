# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 399M 2009-02-02 22:29:31Z (lokal) $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of PatchPanel"""

__version__ = "$Id: template.py_cog 399M 2009-02-02 22:29:31Z (lokal) $"

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
from org.ict_ok.components.patchpanel.interfaces import \
    IAddPatchPanel, IPatchPanel, IPatchPanelFolder
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import Component
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.rack.rack import Rack_PatchPanels_RelManager
from org.ict_ok.components.patchport.interfaces import IPatchPort

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




class PatchPanel(Component):
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
    fullTextSearchFields.extend(Component.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(PatchPanel)
        for (name, value) in data.items():
            if name in IPatchPanel.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        refAttributeNames = getRefAttributeNames(PatchPanel)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class PatchPanelFolder(Superclass, Folder):
    implements(IPatchPanelFolder,
               IImportCsvData,
               IImportXlsData,
               IAddPatchPanel)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
