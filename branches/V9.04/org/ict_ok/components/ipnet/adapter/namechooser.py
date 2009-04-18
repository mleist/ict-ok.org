# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: namechooser.py 273M 2009-04-16 11:09:07Z (lokal) $
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of name chooser
"""

__version__ = "$Id: namechooser.py 273M 2009-04-16 11:09:07Z (lokal) $"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from zope.app.container.interfaces import INameChooser

# ict_ok.org imports
from org.ict_ok.components.superclass.adapter.namechooser import NameChooser
from org.ict_ok.components.ipnet.interfaces import IIpNet

_ = MessageFactory('org.ict_ok')


class IpNetNameChooser(NameChooser):
    """INameChooser adapter."""

    implements(INameChooser)
    adapts(IIpNet)
