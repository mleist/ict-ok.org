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

# ict_ok.org imports
from org.ict_ok.components.superclass.adapter.search import \
     Searchable as SuperSearchable
from org.ict_ok.components.interface.interfaces import \
     IInterface, convertIpV4
from org.ict_ok.components.interface.interface import Interface

_ = MessageFactory('org.ict_ok')


class Searchable(SuperSearchable):
    """Searchable-Adapter."""

    implements(ISearchableText)
    adapts(IInterface)

    def __init__(self, context):
        SuperSearchable.__init__(self, context)

    def getSearchableInterfaceOid(self):
        """
        get Object id as string for catalog
        """
        return self.context.getObjectId()

    def getSearchableInterfaceIp(self):
        return convertIpV4(self.context.ipv4List)

    def getSearchableInterfaceMac(self):
        return self.context.mac

    def getFullTextSearchFields(self):
        """
        """
        return Interface.fullTextSearchFields
