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
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor
from org.ict_ok.components.superclass.interfaces import ITicker


class Ticker(object):
    """Ticker-Adapter."""

    implements(ITicker)
    adapts(IAdmUtilSupervisor)

    def __init__(self, context):
        self.context = context
        self.db = None

    def triggered(self):
        """
        got ticker event from ticker thread
        """
        pass
        #print "Supervisor: '%s' triggered!!" % self.context
        
    def triggerMin(self):
        """
        got ticker event from ticker thread every minute
        """
        print "Supervisor: '%s' triggerMin!!" % self.context
        self.context.appendEventHistory(u'minute ticker')
        #self.context.packDbByTicker(self.db)
        pass

    def triggerHour(self):
        """
        got ticker event from ticker thread every hour
        """
        pass

    def triggerDay(self):
        """
        got ticker event from ticker thread every day
        """
        pass

    def triggerMonth(self):
        """
        got ticker event from ticker thread every month
        """
        pass

    def triggerYear(self):
        """
        got ticker event from ticker thread every year
        """
        pass
