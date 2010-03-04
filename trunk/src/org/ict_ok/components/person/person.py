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

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.person.interfaces import IPerson
from org.ict_ok.components.person.interfaces import IPersonFolder
from org.ict_ok.components.person.interfaces import IAddPerson
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.contact_item.contact_item import ContactItem
from org.ict_ok.components.organisational_unit.interfaces import \
    IOrganisationalUnit

def AllPersonTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IPerson)

def AllPersons(dummy_context):
    return AllComponents(dummy_context, IPerson)

Persons_OrganisationalUnits_RelManager = \
       FieldRelationManager(IPerson['inOUs'],
                            IOrganisationalUnit['members'],
                            relType='members:inOUs')


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
    inOUs = RelationPropertyOut(\
         Persons_OrganisationalUnits_RelManager)

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

    def getRefAttributeNames(self):
        return getRefAttributeNames(Person)

    def store_refs(self, **data):
        ContactItem.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)

    def getDisplayTitle(self):
        """ display text for some views
        """
        return u'%s %s %s' % (self.title, self.firstName, self.lastName)


class PersonFolder(ComponentFolder):
    implements(IPersonFolder,
               IAddPerson)
    contentFactory = Person
    shortName = "person folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
