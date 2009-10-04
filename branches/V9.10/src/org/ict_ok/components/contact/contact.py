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
from org.ict_ok.components.contact.interfaces import IContact
from org.ict_ok.components.contact.interfaces import IContactFolder
from org.ict_ok.components.contact.interfaces import IAddContact
from org.ict_ok.components.component import Component
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.work_order.work_order import WorkOrder_Contacts_RelManager
from org.ict_ok.components.work_order.interfaces import IWorkOrder
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


class ContactFolder(Superclass, Folder):
    implements(IContactFolder,
               IImportCsvData,
               IImportXlsData,
               IAddContact)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
