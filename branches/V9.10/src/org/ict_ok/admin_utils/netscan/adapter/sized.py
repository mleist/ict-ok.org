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
"""Adapter implementation of size-methods
"""

__version__ = "$Id$"

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.size.interfaces import ISized
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.admin_utils.netscan.interfaces import INetScan

_ = MessageFactory('org.ict_ok')


class NetScanSized(object):
    """ISized adapter."""

    implements(ISized)
    adapts(INetScan)

    def __init__(self, context):
        self.context = context

    def sizeForSorting(self):
        """See `ISized`"""
        if self.context.scannerSet:
            return ('item', len(self.context.scannerSet))
        else:
            return 0

    def sizeForDisplay(self):
        """See `ISized`"""
        if self.context.scannerSet:
            size = _('%d scanner' % len(self.context.scannerSet))
        else:
            size = _('no scanner')
        return size
