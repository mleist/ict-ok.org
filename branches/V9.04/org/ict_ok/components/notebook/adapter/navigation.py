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
from org.ict_ok.components.notebook.interfaces import INotebook

_ = MessageFactory('org.ict_ok')


class Navigation(SuperNavigation):
    """navigation-Adapter."""

    implements(INavigation)
    adapts(INotebook)
    
    def getContextObjList(self, preList=None, postList=None):
        """
        get an Object list of all interesting objects in the context
        """
        retList = []
        if preList is not None:
            retList.extend(preList)
        retList.append((None, None, zapi.getParent(self.context)))
        if self.context.room is not None:
            retList.append(('room', _(u'Room'), self.context))
        if len(self.context.interfaces) > 0:
            retList.append(('interfaces', _(u'Interfaces'), self.context))
        if len(self.context.osoftwares) > 0:
            retList.append(('osoftwares', _(u'Operating Software'), self.context))
        if len(self.context.appsoftwares) > 0:
            retList.append(('appsoftwares', _(u'Application Software'), self.context))
        if len(self.context.logicalDevices) > 0:
            retList.append(('logicalDevices', _(u'Logical Devices'), self.context))
        if len(self.context.physicalMedia) > 0:
            retList.append(('physicalMedia', _(u'Physical Media'), self.context))
        if len(self.context.contracts) > 0:
            retList.append(('contracts', _(u'Contracts'), self.context))
        if len(self.context.requirements) > 0:
            retList.append(('requirements', _(u'Requirements'), self.context))
        if postList is not None:
            retList.extend(postList)
        
        return retList
