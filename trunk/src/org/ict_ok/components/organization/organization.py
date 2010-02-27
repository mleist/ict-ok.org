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
"""implementation of Organization"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports
from lovely.relation.property import RelationPropertyOut

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.organization.interfaces import IOrganization
from org.ict_ok.components.organization.interfaces import IOrganizationFolder
from org.ict_ok.components.organization.interfaces import IAddOrganization
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.contact_item.contact_item import ContactItem
from org.ict_ok.components.organisational_unit.organisational_unit import \
    OrganisationalUnit_OrganisationalUnits_RelManager

def AllOrganizationTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IOrganization)

def AllOrganizations(dummy_context):
    return AllComponents(dummy_context, IOrganization)


class Organization(ContactItem):
    """
    the template instance
    """
    implements(IOrganization)
    shortName = "organization"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    name = FieldProperty(IOrganization['name'])
    subOUs = RelationPropertyOut(\
         OrganisationalUnit_OrganisationalUnits_RelManager)

    fullTextSearchFields = ['name']
    fullTextSearchFields.extend(ContactItem.fullTextSearchFields)
        

    def __init__(self, **data):
        """
        constructor of the object
        """
        ContactItem.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Organization)
        for (name, value) in data.items():
            if name in IOrganization.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Organization)

    def store_refs(self, **data):
        ContactItem.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class OrganizationFolder(ComponentFolder):
    implements(IOrganizationFolder,
               IAddOrganization)
    contentFactory = Organization

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
