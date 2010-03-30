# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: search.py_cog 506 2009-04-30 14:24:56Z markusleist $
#
# pylint: disable-msg=E0611,W0212
#
"""Adapter implementation of search-methods for Contact"""

__version__ = "$Id: search.py_cog 506 2009-04-30 14:24:56Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.index.text.interfaces import ISearchableText
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.contact.interfaces import IContact
from org.ict_ok.components.contact.contact import Contact
from org.ict_ok.components.superclass.adapter.search import \
     Searchable as SuperSearchable

_ = MessageFactory('org.ict_ok')


class Searchable(SuperSearchable):
    """Searchable-Adapter."""

    implements(ISearchableText)
    adapts(IContact)

    def __init__(self, context):
        SuperSearchable.__init__(self, context)

    def getSearchableContactOid(self):
        """
        get Object id as string for catalog
        """
        return (self.context.getObjectId(),)


    def getFullTextSearchFields(self):
        """
        """
        return Contact.fullTextSearchFields
