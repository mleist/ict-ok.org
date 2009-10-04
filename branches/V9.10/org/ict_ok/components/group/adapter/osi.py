# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <i_am@not-there.org>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of state-methods for Group"""

__version__ = "$Id$"

# zope imports
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.group.interfaces import IGroup
from org.ict_ok.osi.interfaces import IPhysicalLayer
from org.ict_ok.osi import osi


class OSIModel(osi.OSIModel):
    """OSI adapter."""

    adapts(IGroup)
    linkedObjects = {}
