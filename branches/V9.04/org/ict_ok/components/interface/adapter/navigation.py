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
from org.ict_ok.components.interface.interfaces import IInterface

_ = MessageFactory('org.ict_ok')


class Navigation(SuperNavigation):
    """navigation-Adapter."""

    implements(INavigation)
    adapts(IInterface)
    
    def getContextObjList(self, preList=None, postList=None):
        """
        get an Object list of all interesting objects in the context
        """
        retList = []
        if preList is not None:
            retList.extend(preList)
        retList.append(zapi.getParent(self.context))
        #retList.append(self.context.device)
        #retList.append(('__parent__', _(u'All IP Addresses'), self.context))
        if len(self.context.device) > 0:
            # (navView, viewTitle, contextObj)
            retList.append(('device', _(u'From Device'), self.context))
        if len(self.context.ipAddresses) > 0:
            # (navView, viewTitle, contextObj)
            retList.append(('ipAddresses', _(u'IP Addresses'), self.context))
        if len(self.context.links) > 0:
            # (navView, viewTitle, contextObj)
            retList.append(('links', _(u'Links'), self.context))

        #print "ddd3: ", self.context.device
        #retList.append(self.context.ipAddresses)
        if postList is not None:
            retList.extend(postList)
        return retList
