# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of Notebook"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Bool, Choice, List

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class ILogicalDevice(Interface):
    """A device object."""

    powerManagementSupported = Bool(
        title = _(u'power managed'),
        description = _(u'the Device can be power managed'),
        required = True)

#    device = Choice(
#        title=_(u'Device'),
#        vocabulary='AllDevices',
#        required=False
#        )

    devices = List(title=_(u"Devices"),
                   value_type=Choice(vocabulary='AllDevices'),
                   required=False,
                   default=[])


class ILogicalDeviceFolder(Interface):
    """Container for Notebook objects
    """
