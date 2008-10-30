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
"""Adapter implementation of size-methods
"""

__version__ = "$Id$"

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.size.interfaces import ISized
from zope.i18nmessageid import MessageFactory
from zope.app.container.interfaces import IContainer

# ict_ok.org imports
from org.ict_ok.components.net.interfaces import INet

_ = MessageFactory('org.ict_ok')


class NetSized(object):
    """ISized adapter."""

    implements(ISized)
    adapts(INet)

    def __init__(self, context):
        self.context = context

    def sizeForSorting(self):
        """See `ISized`"""
        return ('item', len(IContainer(self.context)))

    def sizeForDisplay(self):
        """See `ISized`"""
        num_hosts = len(IContainer(self.context))
        if num_hosts == 1:
            return _('1 host')
        return _('%d hosts' % num_hosts)
