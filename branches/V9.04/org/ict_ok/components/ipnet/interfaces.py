# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0213,W0232
#
"""Interface of IpNet"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.interface import Attribute, Invalid, invariant
from zope.schema import Choice, List, Set
from zope.i18nmessageid import MessageFactory
from zope.app.container.constraints import contains

# ict_ok.org imports
from org.ict_ok.schema.ipvalid import NetIpValid
from org.ict_ok.schema.IPy import IP

_ = MessageFactory('org.ict_ok')


class IIpNet(Interface):
    """A network object."""

    contains('org.ict_ok.components.host.interfaces.IHost')

    ipv4 = NetIpValid(
        min_length = 1,
        max_length = 30,
        title = _("IpNetwork IP"),
        description = _("IP address of the IpNetwork."),
        default = u"0.0.0.0/24",
        readonly = False,
        required = True)
    
    ipAddresses = List(
        title = _(u'IP Addresses'),
        value_type=Choice(vocabulary='AllUnusedOrUsedIpNetIpAddresses'),
        default=[],
        required = False)

    parentnet = Choice(
        title = _(u'Parent net'),
        vocabulary = 'AllIpNets',
        required = False)

    subnets = List(
        title = _(u'Sub nets'),
        value_type=Choice(vocabulary='AllValidSubIpNets'),
        default=[],
        required = False)

    @invariant
    def ensureSubnetInIpNet(obj):
        """publicKey must be valid PEM string
        """
        if obj.parentnet is not None:
            if IIpNet.providedBy(obj.parentnet):
                parentnet = IP(obj.parentnet.ipv4)
            else:
                parentnet = IP(obj.parentnet)
            mynet = IP(obj.ipv4)
            if not mynet in parentnet:
                raise Invalid(u"'%s' not in '%s'" % (obj.ipv4, obj.parentnet.ipv4))
        if obj.subnets is not None:
            mynet = IP(obj.ipv4)
            for subnet_obj in obj.subnets:
                subnet = IP(subnet_obj.ipv4)
                if not subnet in mynet:
                    raise Invalid(u"'%s' not in '%s'" % (subnet_obj.ipv4, obj.ipv4))
        
    def containsIp(ipString):
        """ is ip(String) part of this network?
        """


class IEventIfEventIpNet(Interface):
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

class IIpNetFolder(Interface):
    """Container for net objects
    """

class IAddIpNet(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllIpNetTemplates",
        required = False)
