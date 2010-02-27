# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Role"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements

# lovely imports
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.role.interfaces import IRole
from org.ict_ok.components.role.interfaces import IRoleFolder
from org.ict_ok.components.role.interfaces import IAddRole
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates
from org.ict_ok.components.contact_item.interfaces import IContactItem

def AllRoleTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IRole)

def AllRoles(dummy_context):
    return AllComponents(dummy_context, IRole)



Roles_ContactItems_RelManager = \
       FieldRelationManager(IRole['contactItems'],
                            IContactItem['roles'],
                            relType='roles:contactItems')


class Role(Component):
    """
    the template instance
    """
    implements(IRole)
    shortName = "role"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    contactItems = RelationPropertyOut(Roles_ContactItems_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(Component.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Role)
        for (name, value) in data.items():
            if name in IRole.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Role)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class RoleFolder(ComponentFolder):
    implements(IRoleFolder,
               IAddRole)
    contentFactory = Role

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
