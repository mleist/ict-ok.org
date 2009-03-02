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
"""implementation of PhysicalComponent"""

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
from org.ict_ok.components.physical_component.interfaces import \
    IPhysicalComponent
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import Component
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents


class PhysicalComponent(Component):
    """
    the template instance
    """
    implements(IPhysicalComponent)
    shortName = "physical_component"

    user = FieldProperty(IPhysicalComponent['user'])
    manufacturer = FieldProperty(IPhysicalComponent['manufacturer'])
    modelType = FieldProperty(IPhysicalComponent['modelType'])
    vendor = FieldProperty(IPhysicalComponent['vendor'])
    deliveryDate = FieldProperty(IPhysicalComponent['deliveryDate'])
    room = FieldProperty(IPhysicalComponent['room'])
    serialNumber = FieldProperty(IPhysicalComponent['serialNumber'])
    inv_id = FieldProperty(IPhysicalComponent['inv_id'])
    documentNumber = FieldProperty(IPhysicalComponent['documentNumber'])
    productionState = FieldProperty(IPhysicalComponent['productionState'])

    fullTextSearchFields = ['user', 'manufacturer', 'modelType',
                            'vendor', 'serialNumber', 'inv_id',
                            'documentNumber']
    fullTextSearchFields.extend(Component.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(PhysicalComponent)
        for (name, value) in data.items():
            if name in IPhysicalComponent.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        refAttributeNames = getRefAttributeNames(PhysicalComponent)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)

