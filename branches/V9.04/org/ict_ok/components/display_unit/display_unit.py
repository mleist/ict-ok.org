# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 465M 2009-03-05 02:48:01Z (lokal) $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of DisplayUnit"""

__version__ = "$Id: template.py_cog 465M 2009-03-05 02:48:01Z (lokal) $"

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
from org.ict_ok.components.display_unit.interfaces import IDisplayUnit
from org.ict_ok.components.display_unit.interfaces import IDisplayUnitFolder
from org.ict_ok.components.display_unit.interfaces import IAddDisplayUnit
from org.ict_ok.components.component import Component
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.osi import osi
from org.ict_ok.components.physical_component.physical_component import \
    PhysicalComponent

def AllDisplayUnitTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IDisplayUnit)

def AllDisplayUnits(dummy_context):
    return AllComponents(dummy_context, IDisplayUnit)







class DisplayUnit(PhysicalComponent):
    """
    the template instance
    """
    implements(IDisplayUnit)
    shortName = "display_unit"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    horizontalResolution = FieldProperty(IDisplayUnit['horizontalResolution'])
    verticalResolution = FieldProperty(IDisplayUnit['verticalResolution'])

    fullTextSearchFields = []
    fullTextSearchFields.extend(PhysicalComponent.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalComponent.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(DisplayUnit)
        for (name, value) in data.items():
            if name in IDisplayUnit.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        PhysicalComponent.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(DisplayUnit)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class DisplayUnitFolder(Superclass, Folder):
    implements(IDisplayUnitFolder,
               IImportCsvData,
               IImportXlsData,
               IAddDisplayUnit)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
