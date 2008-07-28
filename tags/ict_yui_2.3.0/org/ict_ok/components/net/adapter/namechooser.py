# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of name chooser
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from zope.app.container.interfaces import INameChooser

# ict_ok.org imports
from org.ict_ok.components.superclass.adapter.namechooser import NameChooser
from org.ict_ok.components.net.interfaces import INet

_ = MessageFactory('org.ict_ok')


class NetNameChooser(NameChooser):
    """INameChooser adapter."""

    implements(INameChooser)
    adapts(INet)
