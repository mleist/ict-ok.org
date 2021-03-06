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
"""Interface of Building"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.schema import TextLine

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class IBuilding(IComponent):
    """A service object."""

    coordinates = TextLine(
        max_length = 80,
        title = _("coordinates"),
        description = _("Coordinates of the building."),
        default = u"",
        required = False)

    gmapsurl = TextLine(
        max_length = 200,
        title = _("GoogleMap URL"),
        description = _("URL of the location at google maps."),
        default = u"",
        required = False)
