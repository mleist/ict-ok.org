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
"""Interface of Net"""

__version__ = "$Id$"

# zope imports
from zope.schema import Choice, Set
from zope.i18nmessageid import MessageFactory
from zope.app.container.constraints import contains

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.components.supernode.interfaces import \
     IEventIfSupernode
from org.ict_ok.schema.ipvalid import NetIpValid

_ = MessageFactory('org.ict_ok')


class INet(IComponent):
    """A network object."""

    contains('org.ict_ok.components.host.interfaces.IHost')

    ipv4 = NetIpValid(
        min_length = 1,
        max_length = 30,
        title = _("Network IP"),
        description = _("IP address of the Network."),
        default = u"0.0.0.0/24",
        readonly = False,
        required = True)
    
    def containsIp(ipString):
        """ is ip(String) part of this network?
        """


class IEventIfEventNet(IEventIfSupernode):
    """ event interface of object """
    
    eventInpObjs_inward_relaying_shutdown = Set(
        title = _("inward relaying shutdown <-"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)
    
    def eventInp_inward_relaying_shutdown(eventMsg):
        """
        forward the event to all objects in this container through the signal filter
        """
