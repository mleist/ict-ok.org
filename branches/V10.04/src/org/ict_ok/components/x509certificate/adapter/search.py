# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611,W0212
#
"""Adapter implementation of search-methods for Outlet"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.index.text.interfaces import ISearchableText
from zope.i18nmessageid import MessageFactory
from zope.security.proxy import removeSecurityProxy

# ict_ok.org imports
from org.ict_ok.components.x509certificate.interfaces import IX509Certificate
from org.ict_ok.components.x509certificate.x509certificate import X509Certificate
from org.ict_ok.components.superclass.adapter.search import \
     Searchable as SuperSearchable

_ = MessageFactory('org.ict_ok')


class Searchable(SuperSearchable):
    """Searchable-Adapter."""

    implements(ISearchableText)
    adapts(IX509Certificate)

    def __init__(self, context):
        SuperSearchable.__init__(self, context)

    def getSearchableOutletOid(self):
        """
        get Object id as string for catalog
        """
        return (self.context.getObjectId(),)


    def getFullTextSearchFields(self):
        """
        """
        return X509Certificate.fullTextSearchFields

    def getSearchableFullText(self):
        """
        get Object id as string for catalog
        """
        stringList = []
        for field in self.getFullTextSearchFields():
            stringList.append(u"%s" % getattr(self.context, field))
        issuerName = removeSecurityProxy(self.context.getIssuerName())
        subject = removeSecurityProxy(self.context.getSubject())
        if issuerName:
            issuerName_str = u', '.join([u"%s=%s" % (i_k, i_v)
                                    for i_k, i_v in issuerName.get_components()])
            stringList.append(issuerName_str)
        if subject:
            subject_str = u', '.join([u"%s=%s" % (i_k, i_v)
                                    for i_k, i_v in subject.get_components()])
            stringList.append(subject_str)
        return u" ".join(stringList)
