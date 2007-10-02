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
"""Interface of Net"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.app.container.constraints import contains

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.schema.ipvalid import IpValid

_ = MessageFactory('org.ict_ok')


class INet(IComponent):
    """A network object."""

    contains('org.ict_ok.components.host.interfaces.IHost')

    ipv4 = IpValid(
        min_length = 1,
        max_length = 30,
        title = _("Network IP"),
        description = _("IP address of the Network."),
        default = u"0.0.0.0/24",
        readonly = False,
        required = True)
    
