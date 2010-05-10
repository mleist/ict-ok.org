# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of IpAddress"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.interface import Attribute, Invalid, invariant
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

# ict_ok.org imports
from org.ict_ok.schema.ipvalid import NetIpValid
from org.ict_ok.schema.IPy import IP

_ = MessageFactory('org.ict_ok')


class IIpAddress(Interface):
    """A IpAddress object."""

    ipv4 = NetIpValid(
        title = _(u'IP Address'),
        description = _(u"IP address of the device."),
        required = True)
        

    hostname = TextLine(
        title = _(u'Hostname'),
        description = _(u"reverse hostname for this IP address."),
        required = False)
        

    interface = Choice(
        title = _(u'Interface'),
        vocabulary = 'AllInterfaces',
        required = False)
        
    ipNet = Choice(
        title = _(u'IP Net'),
        vocabulary = 'AllIpNets',
        required = False)

    @invariant
    def ensureIpAddressInIpNet(obj):
        """address must be in network
        """
        if obj.ipNet is not None:
            ipNet = IP(obj.ipNet.ipv4)
            mynet = IP(obj.ipv4)
            if not mynet in ipNet:
                raise Invalid(u"'%s' not in '%s'" % (obj.ipv4, obj.ipNet.ipv4))
        
    def trigger_online():
        """
        trigger workflow
        """


class IIpAddressFolder(Interface):
    """Container for IpAddress objects
    """


class IAddIpAddress(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllIpAddressTemplates",
        required = False)
