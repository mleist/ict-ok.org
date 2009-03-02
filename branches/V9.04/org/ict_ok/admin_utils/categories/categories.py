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
from zope.app.container.interfaces import IOrderedContainer

# ict_ok.org imports
from org.ict_ok.admin_utils.categories.interfaces import \
     IAdmUtilCategories, IAdmUtilCatHostGroup
from org.ict_ok.components.superclass.superclass import Superclass


class AdmUtilCategories(OrderedContainer, Superclass):
    """Implementation of local Categories-Utility"""

    implements(IAdmUtilCategories)

    def __init__(self):
        Superclass.__init__(self)
        OrderedContainer.__init__(self)
        self.ikRevision = __version__

    def getHostGroups(self):
        hostGroups = []
        for (oid, obj) in self.items():
            if IAdmUtilCatHostGroup.providedBy(obj):
                hostGroups.append(obj)
        return hostGroups
