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
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, List, TextLine

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IBuilding(Interface):
    """A service object."""
    
    location = Choice(
        title=_(u'Location'),
        vocabulary='AllLocations',
        required=False
        )
    
    rooms = List(title=_(u"Rooms"),
                      value_type=Choice(vocabulary='AllUnusedOrUsedBuildingRooms'),
                      required=False,
                      default=[])

    coordinates = TextLine(
        max_length = 80,
        title = _("coordinates"),
        description = _("Coordinates of the building."),
        default = u"",
        required = False)

    gmapsurl = TextLine(
        max_length = 500,
        title = _("GoogleMap URL"),
        description = _("URL of the location at google maps."),
        default = u"",
        required = False)

    gmapcode = TextLine(
        max_length = 1500,
        title = _("GoogleMap HTML-Code"),
        description = _("HTML Code of the location at google maps."),
        default = u"",
        required = False)

class IBuildingFolder(Interface):
    """Container for Building objects
    """

class IAddBuilding(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllBuildingTemplates",
        required = False)
