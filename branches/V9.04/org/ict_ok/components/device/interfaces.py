# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of Notebook"""


__version__ = "$Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, List, TextLine
from zope.app.folder.interfaces import IFolder

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class IDevice(IComponent):
    """A device object."""

    manufacturer = TextLine(
        max_length = 200,
        title = _("Manufacturer"),
        description = _("Name/Address of the manufacturer."),
        required = False)
    vendor = TextLine(
        max_length = 500,
        title = _("Vendor"),
        description = _("Name/Address of the vendor."),
        default = u"",
        required = False)
    
    room = Choice(
        title=_(u'Room'),
        vocabulary='AllRooms',
        required=False
        )
    
    osoftwares = List(title=_(u"Operating software"),
                      value_type=Choice(vocabulary='AllUnusedOrUsedDeviceOperatingSoftwares'),
                      required=False,
                      default=[])
    
    appsoftwares = List(title=_(u"Application software"),
                      value_type=Choice(vocabulary='AllUnusedOrUsedDeviceApplicationSoftwares'),
                      required=False,
                      default=[])


class IDeviceFolder(ISuperclass, IFolder):
    """Container for Notebook objects
    """
