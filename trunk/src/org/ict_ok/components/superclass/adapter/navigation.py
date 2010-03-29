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
"""Adapter implementation of navigation-methods
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from zope.app import zapi
from zope.site.interfaces import IFolder, IRootFolder
from zope.security import canAccess

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import \
    ISuperclass, INavigation

_ = MessageFactory('org.ict_ok')


class Navigation(object):
    """navigation-Adapter."""

    implements(INavigation)
    adapts(ISuperclass)

    def __init__(self, context):
        self.context = context

    def getContextObjList(self, preList=None, postList=None):
        """
        get an Object list of all interesting objects in the context
        """
        retList = []
        if preList is not None:
            retList.extend(preList)
        try:
            parentObj = zapi.getParent(self.context)
            if parentObj is not None and canAccess(parentObj, '__len__'):
                retList.append((None, None, parentObj))
        except Exception:
            print "111e"
            import traceback
            print traceback.format_exc()
        if postList is not None:
            retList.extend(postList)
        return retList

    def getViewObjList(self, viewName):
        """
        """
        retList = []
        value = getattr(self.context, viewName, None)
        if viewName == '__parent__':
            retList.extend(value.values())
        else:
            if value is not None:
                retList.extend(value)
            else:
                locValue = getattr(self, viewName, None)
        return retList


class RootNavigation(Navigation):
    implements(INavigation)
    adapts(IRootFolder)
