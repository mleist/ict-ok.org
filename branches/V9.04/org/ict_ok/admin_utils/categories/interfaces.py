# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=W0232
#
"""Interface of Object-Message-Queue-Utility"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import TextLine, Set
from zope.app.container.interfaces import IOrderedContainer

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class IAdmUtilCategories(Interface):
    """A configuration utility."""

class IAdmUtilCatHostGroup(Interface):
    """A host group entry.
    """
#    def canBeDeleted():
#        """
#        a object can be deleted with normal delete permission
#        special objects can overload this for special delete rules
#        (e.g. IAdmUtilCatHostGroup)
#        return True or False
#        """
    def isUsedIn():
        """
        this object is used at least in one host (returns object list)
        """
