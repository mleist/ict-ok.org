# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of host object"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Set

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import \
     IEventIfSupernode
from org.ict_ok.components.host.interfaces import IHost

_ = MessageFactory('org.ict_ok')


class IHostMgeUps(IHost):
    """A MGE UPS object."""

class IEventIfHostMgeUps(IEventIfSupernode):
    """ event interface of object """
    eventOutObjs_onBattery = Set(
        title = _("on battery ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    eventOutObjs_powerReturned = Set(
        title = _("power returned ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)
    def eventOut_onBattery(self):
        """ sends 'on battery' event """
    def eventOut_powerReturned(self):
        """ sends 'power returned' event """
