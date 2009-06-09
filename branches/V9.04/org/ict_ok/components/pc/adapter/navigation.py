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
from org.ict_ok.components.pc.interfaces import IPersonalComputer
from org.ict_ok.components.superclass.interfaces import \
    INavigation
from org.ict_ok.components.superclass.adapter.navigation import \
    Navigation as SuperNavigation


_ = MessageFactory('org.ict_ok')


class Navigation(SuperNavigation):
    """navigation-Adapter."""

    implements(INavigation)
    adapts(IPersonalComputer)

    def __init__(self, context):
        self.context = context

    def getContextObjList(self, preList=[], postList=[]):
        """
        get an Object list of all interesting objects in the context
        """
        retList = []
        #retList.extend(preList)
        #retList.extend(list(self.context.interfaces))
        #retList.extend(list(self.context.physicalMedia))
        retList.append((self.context, 'physicalMedia', u'physical media'))
        #retList.extend(SuperNavigation.getContextObjList(self))
        #retList.extend(postList)
        return retList
