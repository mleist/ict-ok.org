# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of state-methods for PatchPanel"""

__version__ = "$Id$"

# zope imports
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

# ict_ok.org imports
from org.ict_ok.components.patchpanel.interfaces import IPatchPanel


@adapter(IPatchPanel, IObjectModifiedEvent)
def update(obj, event):
    """
    Update for:
        the room-refs of all patch-ports
    """
    if event is not None:
        for i in event.descriptions:
            modAttributes = set(i.attributes)
            if 'room' in modAttributes:
                for patchport in obj.patchports:
                    patchport.room = obj.room
