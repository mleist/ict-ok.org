# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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

# phython imports

# zope imports
from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from zope.dublincore.interfaces import IZopeDublinCore, IWriteZopeDublinCore

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import IBrwsOverview

_ = MessageFactory('org.ict_ok')


class BrwsOverview(object):
    """Searchable-Adapter."""

    implements(IBrwsOverview)

    def __init__(self, context):
        self.context = context

    def getTitle(self):
        """
        get Title of the Object
        """
        return IZopeDublinCore(self.context).title

    def setTitle(self, title):
        """
        set Title of the Object
        """
        IWriteZopeDublinCore(self.context).title = title
