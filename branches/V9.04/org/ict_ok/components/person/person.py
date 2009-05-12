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
"""implementation of Person"""

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
from org.ict_ok.components.person.interfaces import IPerson
from org.ict_ok.components.person.interfaces import IPersonFolder
from org.ict_ok.components.person.interfaces import IAddPerson
from org.ict_ok.components.component import Component
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.contact_item.contact_item import ContactItem

def AllPersonTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IPerson)

def AllPersons(dummy_context):
    return AllComponents(dummy_context, IPerson)







class Person(ContactItem):
    """
    the template instance
    """
    implements(IPerson)
    shortName = "person"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    firstName = FieldProperty(IPerson['firstName'])
    lastName = FieldProperty(IPerson['lastName'])
    title = FieldProperty(IPerson['title'])

    fullTextSearchFields = ['firstName', 'lastName', 'title']
    fullTextSearchFields.extend(ContactItem.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        ContactItem.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Person)
        for (name, value) in data.items():
            if name in IPerson.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        ContactItem.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(Person)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class PersonFolder(Superclass, Folder):
    implements(IPersonFolder,
               IImportCsvData,
               IImportXlsData,
               IAddPerson)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
