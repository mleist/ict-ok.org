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
from zope.interface import implements, providedBy
from zope.component import adapts
from zope.index.text.interfaces import ISearchableText
from zope.index.keyword.interfaces import IKeywordQuerying
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.superclass.superclass import Superclass

_ = MessageFactory('org.ict_ok')


class Searchable(object):
    """Searchable-Adapter."""

    implements(ISearchableText)
    adapts(ISuperclass)

    def __init__(self, context):
        self.context = context

    def getSearchableOid(self):
        """
        get Object id as string for catalog
        """
        return (self.context.getObjectId(),)

    def getSearchableComments(self):
        """
        get object comment as string for catalog
        """
        if not self.context.ikComment:
            return ""
        return self.context.ikComment

    def getSearchableNotes(self):
        """
        get object notes as string for catalog
        """
        if not self.context.ikNotes:
            return ""
        return u' '.join([unicode(note) for note in self.context.ikNotes])

    def getFullTextSearchFields(self):
        """
        """
        return Superclass.fullTextSearchFields
    
    def getSearchableFullText(self):
        """
        get Object id as string for catalog
        """
        stringList = []
        for field in self.getFullTextSearchFields():
            #print u"%s : '%s'" % (field, getattr(self.context, field))
            stringList.append(u"%s" % getattr(self.context, field))
        return u" ".join(stringList)

class SearchableKeywords(object):
    """Searchable-Adapter."""

    implements(IKeywordQuerying)
    adapts(ISuperclass)

    def __init__(self, context):
        self.context = context

    def getSearchableInterfaces(self):
        """
        get a list of provided interfaces
        """
        from zope.security.proxy import removeSecurityProxy
        prov_by = removeSecurityProxy(providedBy(self.context))
        return [unicode(i.__module__+'.'+i.__name__) \
                for i in prov_by.interfaces()]
