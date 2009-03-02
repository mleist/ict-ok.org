# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: search.py 394 2009-01-06 15:12:30Z markusleist $
#
# pylint: disable-msg=E0611,W0212
#
"""Adapter implementation of search-methods for Outlet"""

__version__ = "$Id: search.py 394 2009-01-06 15:12:30Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.index.text.interfaces import ISearchableText
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.physical_link.interfaces import IPhysicalLink
from org.ict_ok.components.physical_link.physical_link import PhysicalLink
from org.ict_ok.components.superclass.adapter.search import \
     Searchable as SuperSearchable

_ = MessageFactory('org.ict_ok')


class Searchable(SuperSearchable):
    """Searchable-Adapter."""

    implements(ISearchableText)
    adapts(IPhysicalLink)

    def __init__(self, context):
        SuperSearchable.__init__(self, context)

    def getSearchablePhysicalLinkOid(self):
        """
        get Object id as string for catalog
        """
        return self.context.getObjectId()

    def getFullTextSearchFields(self):
        """
        """
        return PhysicalLink.fullTextSearchFields
