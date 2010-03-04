# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <i_am@not-there.org>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Group"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements

# lovely imports
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.group.interfaces import IGroup
from org.ict_ok.components.group.interfaces import IGroupFolder
from org.ict_ok.components.group.interfaces import IAddGroup
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates
from org.ict_ok.components.contact_item.interfaces import IContactItem

def AllGroupTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IGroup)

def AllGroups(dummy_context):
    return AllComponents(dummy_context, IGroup)



Group_ContactItems_RelManager = \
       FieldRelationManager(IGroup['contactItems'],
                            IContactItem['groups'],
                            relType='groups:contactItems')




class Group(Component):
    """
    the template instance
    """
    implements(IGroup)
    shortName = "group"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    contactItems = RelationPropertyOut(Group_ContactItems_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(Component.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Group)
        for (name, value) in data.items():
            if name in IGroup.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Group)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class GroupFolder(ComponentFolder):
    implements(IGroupFolder,
               IAddGroup)
    contentFactory = Group
    shortName = "group folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
