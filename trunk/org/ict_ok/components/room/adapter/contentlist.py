# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
#
"""Adapter implementation of size-methods
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from zope.app.catalog.interfaces import ICatalog

# ict_ok.org imports
from org.ict_ok.components.room.interfaces import IRoom
from org.ict_ok.components.supernode.interfaces import IContentList

_ = MessageFactory('org.ict_ok')


class ContentList(object):
    """content-objects-adapter."""

    implements(IContentList)
    adapts(IRoom)

    def __init__(self, context):
        self.context = context
        
    def getContentList(self):
        """get the List of Content objects
        """
        my_catalog = zapi.getUtility(ICatalog)
        return list(my_catalog.searchResults(\
            host_room_oid_index=self.context.objectID))
