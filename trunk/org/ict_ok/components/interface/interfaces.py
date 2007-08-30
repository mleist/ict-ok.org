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
"""Interface of Interface"""

__version__ = "$Id$"

# zope imports
from zope.schema import Choice, List
from zope.i18nmessageid import MessageFactory
from zope.app.container.constraints import contains

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.schema.ipvalid import IpValid
from org.ict_ok.schema.macvalid import MacValid

_ = MessageFactory('org.ict_ok')


class IInterface(ISupernode):
    """A interface object."""

    contains('org.ict_ok.components.service.interfaces.IService',
             'org.ict_ok.components.snmpvalue.interfaces.ISnmpValue')

    netType = Choice(
        title = _("interface type"),
        description = _("Networktype of this interface (OSI Layer1-2)"),
        default = "ethernet",
        values = ['ethernet', 'fddi', 'wlan', 'token bus', 'token ring'],
        required = True)

    mac = MacValid(
        max_length=40,
        title=_("MAC address"),
        description=_("MAC address of the host."),
        default=u"00:00:00:00:00:00",
        required=False)

    ipv4List = List (
        title = _("IPv4 addresses"),
        description = _("list of all configured IPv4 addresses"),
        value_type = IpValid(
            min_length=1,
            max_length=30,
            title=_("IP address"),
            description=_("IP address of the host."),
            default=u"192.168.1.100",
            required=True),
        required = False)

    #connectedInterfaces