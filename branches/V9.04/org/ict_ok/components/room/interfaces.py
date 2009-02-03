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
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, List, TextLine 
from zope.app.folder.interfaces import IFolder

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class IRoom(IComponent):
    """A service object."""

    building = Choice(
        title=_(u'Building'),
        vocabulary='AllBuildings',
        required=False
        )

    devices = List(title=_(u"Devices"),
        value_type=Choice(vocabulary='AllUnusedOrUsedRoomDevices'),
        required=False,
        default=[])
    
    physicalConnectors = List(title=_(u"Physical connectors"),
        value_type=Choice(vocabulary='AllUnusedOrUsedRoomPhysicalConnectors'),
        required=False,
        default=[])
    
    racks = List(title=_(u"Racks"),
        value_type=Choice(vocabulary='AllUnusedOrUsedRoomRacks'),
        required=False,
        default=[])
    
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

class IRoomFolder(ISuperclass, IFolder):
    """Container for room objects
    """

class IAddRoom(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllRoomTemplates",
        required = False)
