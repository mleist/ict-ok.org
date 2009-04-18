# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: sized.py 145M 2009-04-16 11:09:08Z (lokal) $
#
# pylint: disable-msg=E0611,W0212
#
"""Adapter implementation of size-methods
"""

__version__ = "$Id: sized.py 145M 2009-04-16 11:09:08Z (lokal) $"

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.size.interfaces import ISized
from zope.i18nmessageid import MessageFactory
from zope.app.container.interfaces import IContainer

# ict_ok.org imports
from org.ict_ok.components.ipnet.interfaces import IIpNet

_ = MessageFactory('org.ict_ok')


class IpNetSized(object):
    """ISized adapter."""

    implements(ISized)
    adapts(IIpNet)

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
