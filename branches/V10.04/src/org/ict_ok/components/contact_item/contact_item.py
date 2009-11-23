# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of ContactItem"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

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
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.contact_item.interfaces import IContactItem
from org.ict_ok.components.contact_item.interfaces import IContactItemFolder
from org.ict_ok.components.contact_item.interfaces import IAddContactItem
from org.ict_ok.components.component import Component
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.contact.contact import Contact_ContactItems_RelManager
from org.ict_ok.components.work_order.work_order import WorkOrder_ContactItems_RelManager
from org.ict_ok.components.contact.interfaces import IContact
from org.ict_ok.components.address.interfaces import IAddress
from org.ict_ok.components.role.role import Roles_ContactItems_RelManager
from org.ict_ok.components.group.group import Group_ContactItems_RelManager
from org.ict_ok.components.contract.contract import \
    Responsible4Contracts_ContactItems_RelManager
from org.ict_ok.components.contract.contract import \
    ClosedContracts_ContactItems_RelManager


def AllContactItemTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IContactItem)

def AllContactItems(dummy_context):
    return AllComponents(dummy_context, IContactItem)

def AllUnusedOrUsedContactContactItems(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IContactItem, 'contact')
def AllUnusedOrUsedWorkOrderContactItems(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IContactItem, 'workOrder')
def AllUnusedOrUsedRolesContactItems(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IContactItem, 'roles')


ContactItem_Addresses_RelManager = \
       FieldRelationManager(IContactItem['adresses'],
                            IAddress['contactItem'],
                            relType='contactItem:adresses')


class ContactItem(Component):
    """
    the template instance
    """
    implements(IContactItem)
    shortName = "contact_item"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    contact = RelationPropertyIn(Contact_ContactItems_RelManager)
    workOrder = RelationPropertyIn(WorkOrder_ContactItems_RelManager)
    adresses = RelationPropertyOut(ContactItem_Addresses_RelManager)
    roles = RelationPropertyIn(Roles_ContactItems_RelManager)
    groups = RelationPropertyIn(Group_ContactItems_RelManager)
    closedContracts = RelationPropertyIn(ClosedContracts_ContactItems_RelManager)
    responsible4Contracts = RelationPropertyIn(Responsible4Contracts_ContactItems_RelManager)
        
    fullTextSearchFields = []
    fullTextSearchFields.extend(Component.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(ContactItem)
        for (name, value) in data.items():
            if name in IContactItem.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(ContactItem)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class ContactItemFolder(Superclass, Folder):
    implements(IContactItemFolder,
               IImportCsvData,
               IImportXlsData,
               IAddContactItem)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
