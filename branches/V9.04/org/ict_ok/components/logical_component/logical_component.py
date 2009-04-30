# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of LogicalComponent"""

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
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.logical_component.interfaces import \
    ILogicalComponent
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import Component
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents



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
