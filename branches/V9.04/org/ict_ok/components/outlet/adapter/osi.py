# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: state.py 394 2009-01-06 15:12:30Z markusleist $
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of OSI-methods for PatchPort"""

__version__ = "$Id: state.py 394 2009-01-06 15:12:30Z markusleist $"

# zope imports
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.outlet.interfaces import IOutlet
from org.ict_ok.osi.interfaces import IPhysicalLayer
from org.ict_ok.osi import osi

class OSIModel(osi.OSIModel):
    """OSI adapter."""

    adapts(IOutlet)
    linkedObjects = {IPhysicalLayer: ['links']}
