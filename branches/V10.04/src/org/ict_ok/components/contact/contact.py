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
"""implementation of Contact"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.interface import implements

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.contact.interfaces import IContact
from org.ict_ok.components.contact.interfaces import IContactFolder
from org.ict_ok.components.contact.interfaces import IAddContact
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.work_order.work_order import WorkOrder_Contacts_RelManager
from org.ict_ok.components.contact_item.interfaces import IContactItem

def AllContactTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IContact)

def AllContacts(dummy_context):
    return AllComponents(dummy_context, IContact)

def AllUnusedOrUsedWorkOrderContacts(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IContact, 'workOrder')

#def AllUnusedOrUsedContactContacts(dummy_context):
    #return AllUnusedOrSelfComponents(dummy_context, IContact, 'workOrder')

Contact_ContactItems_RelManager = \
       FieldRelationManager(IContact['contactItems'],
                            IContactItem['contact'],
                            relType='contact:contactItems')


class Contact(Component):
    """
    the template instance
    """
    implements(IContact)
    shortName = "contact"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    workOrder = RelationPropertyIn(WorkOrder_Contacts_RelManager)
    contactItems = RelationPropertyOut(Contact_ContactItems_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(Component.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Contact)
        for (name, value) in data.items():
            if name in IContact.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class ContactFolder(ComponentFolder):
    implements(IContactFolder,
               IAddContact)
    contentFactory = Contact
    shortName = "contact folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
