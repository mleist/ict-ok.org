# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0702,W0221
#
"""implementation of a "Object-Message-Queue-Utility" 
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.app.container.ordered import OrderedContainer

# lovely imports
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.admin_utils.categories.interfaces import \
     IAdmUtilCategories, ICategory
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.categories.rel_managers import \
    Categories_Components_RelManager, Categories_Requirements_RelManager
from org.ict_ok.components.component import AllComponents
#from org.ict_ok.admin_utils.compliance.interfaces import IRequirement


def AllCategories(dummy_context):
    return AllComponents(dummy_context, ICategory)


class AdmUtilCategories(OrderedContainer, Superclass):
    """Implementation of local Categories-Utility"""

    implements(IAdmUtilCategories)

    def __init__(self):
        Superclass.__init__(self)
        OrderedContainer.__init__(self)
        self.ikRevision = __version__


class Category(Supernode):
    """Implementation of host group entry."""

    implements(ICategory)
    components = RelationPropertyOut(Categories_Components_RelManager)
    requirements = RelationPropertyOut(Categories_Requirements_RelManager)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Supernode.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Category)
        for (name, value) in data.items():
            if name in ICategory.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        refAttributeNames = getRefAttributeNames(Category)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)
