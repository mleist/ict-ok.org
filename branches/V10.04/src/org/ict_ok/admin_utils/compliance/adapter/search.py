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
from org.ict_ok.admin_utils.compliance.interfaces import IRequirement

_ = MessageFactory('org.ict_ok')


class Searchable(object):
    """Searchable-Adapter."""

    implements(ISearchableText)
    adapts(IRequirement)

    def __init__(self, context):
        self.context = context

    def getSearchableOid(self):
        """
        get Object id as string for catalog
        """
        return (self.context.getObjectId(),)
