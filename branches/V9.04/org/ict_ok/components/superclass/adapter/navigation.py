# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611,W0212
#
"""Adapter implementation of search-methods
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.index.text.interfaces import ISearchableText
from zope.i18nmessageid import MessageFactory
from zope.app import zapi

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import \
    ISuperclass, INavigation
from org.ict_ok.components.superclass.superclass import Superclass

_ = MessageFactory('org.ict_ok')


class Navigation(object):
    """navigation-Adapter."""

    implements(INavigation)
    adapts(ISuperclass)

    def __init__(self, context):
        self.context = context

    def getContextObjList(self, preList=[], postList=[]):
        """
        get an Object list of all interesting objects in the context
        """
        retList = []
        retList.extend(preList)
        retList.append(zapi.getParent(self.context))
        retList.append(zapi.getParent(self.context))
        retList.extend(postList)
        return retList
