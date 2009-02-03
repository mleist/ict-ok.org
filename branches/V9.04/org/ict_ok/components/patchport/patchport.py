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
"""implementation of PatchPort"""

__version__ = "$Id: template.py_cog 399M 2009-02-02 22:29:31Z (lokal) $"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.folder import Folder

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.patchport.interfaces import \
    IPatchPort, IPatchPortFolder, IAddPatchPort
from org.ict_ok.components.component import Component
from org.ict_ok.components.physical_connector.physical_connector import \
    PhysicalConnector, PhysicalConnectorFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.patchpanel.patchpanel import PatchPanel_PatchPorts_RelManager
from org.ict_ok.components.patchpanel.interfaces import IPatchPanel

def AllPatchPortTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IPatchPort)

def AllPatchPorts(dummy_context):
    return AllComponents(dummy_context, IPatchPort)

def AllUnusedOrUsedPatchPanelPatchPorts(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IPatchPort, 'patchpanel')


class PatchPort(PhysicalConnector):
    """
    the template instance
    """
    implements(IPatchPort)
    shortName = "patchport"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    patchpanel = RelationPropertyIn(PatchPanel_PatchPorts_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(Component.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalConnector.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(PatchPort)
        for (name, value) in data.items():
            if name in IPatchPort.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        PhysicalConnector.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(PatchPort)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class PatchPortFolder(PhysicalConnectorFolder):
    implements(IPatchPortFolder,
               IAddPatchPort)
    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalConnectorFolder.__init__(self, **data)
