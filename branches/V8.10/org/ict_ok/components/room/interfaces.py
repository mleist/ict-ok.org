# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of Room"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.schema import TextLine

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class IRoom(IComponent):
    """A service object."""

    level = TextLine(
        max_length = 80,
        title = _("Level"),
        description = _("Level of the room."),
        default = u"",
        required = False)

    coordinates = TextLine(
        max_length = 80,
        title = _("coordinates"),
        description = _("Coordinates of the room."),
        default = u"",
        required = False)
