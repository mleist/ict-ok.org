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

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import INavigation
from org.ict_ok.components.superclass.adapter.navigation import \
    Navigation as SuperNavigation
from org.ict_ok.components.appsoftware.interfaces import IApplicationSoftware

_ = MessageFactory('org.ict_ok')


class Navigation(SuperNavigation):
    """navigation-Adapter."""

    implements(INavigation)
    adapts(IApplicationSoftware)
    
    def getContextObjList(self, preList=None, postList=None):
        """
        get an Object list of all interesting objects in the context
        """
        retList = []
        if preList is not None:
            retList.extend(preList)
        retList.append((None, None, zapi.getParent(self.context)))
        if self.context.device is not None:
            retList.append(('device', _(u'Device'), self.context))
        if postList is not None:
            retList.extend(postList)
        print retList
        return retList
