# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: osi.py_cog 506 2009-04-30 14:24:56Z markusleist $
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of state-methods for Product"""

__version__ = "$Id: osi.py_cog 506 2009-04-30 14:24:56Z markusleist $"

# zope imports
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.product.interfaces import IProduct
from org.ict_ok.osi.interfaces import IPhysicalLayer
from org.ict_ok.osi import osi


class OSIModel(osi.OSIModel):
    """OSI adapter."""

    adapts(IProduct)
    linkedObjects = {}
