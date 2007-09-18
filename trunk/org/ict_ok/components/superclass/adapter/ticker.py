# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of size-methods
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass, ITicker


class Ticker(object):
    """Ticker-Adapter."""

    implements(ITicker)
    adapts(ISuperclass)

    def __init__(self, context):
        self.context = context

    def triggered(self):
        """
        got ticker event from ticker thread
        """
#        print "%s triggered!!" % self.context
        self.context.tickerEvent()
