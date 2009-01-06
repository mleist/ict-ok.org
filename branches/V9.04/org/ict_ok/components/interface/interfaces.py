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
"""Interface of Interface"""

__version__ = "$Id$"

# zope imports
from zope.app import zapi
from zope.schema import Choice, List
from zope.interface import Attribute, Interface, Invalid, invariant
from zope.i18nmessageid import MessageFactory
from zope.app.catalog.interfaces import ICatalog
from zope.app.container.constraints import contains

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.schema.ipvalid import HostIpValid
from org.ict_ok.schema.macvalid import MacValid

_ = MessageFactory('org.ict_ok')


def convertIpV4(inp):
    """convert string or list of strings from ipv4-addresses """
    try:
        #list of ipv4 addresses
        return ' '.join([str(ip).replace(".", "_").replace("/", "__") \
                         for ip in inp])
    except Exception:
        return str(inp).replace(".", "_").replace("/", "__")


class IInterface(IComponent):
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

    #wait for z3c.form list of textlines
    ipv4List = List (
        title = _("IPv4 addresses"),
        description = _("list of all configured IPv4 addresses"),
        value_type = HostIpValid(
            min_length=1,
            max_length=30,
            title=_("IP address"),
            description=_("IP address of the host."),
            default=u"192.168.1.100",
            required=True),
        default = [],
        required = False)
    #ipv4List = HostIpValid(
            #min_length=1,
            #max_length=30,
            #title=_("IP address"),
            #description=_("IP address of the host."),
            #default=u"192.168.1.100",
            #required=False)

    #connectedInterfaces

    @invariant
    def ensureMyIpInNetIpRange(intfc):
        if intfc.netType == 'ethernet' and \
           intfc.__context__ is not None and \
           intfc.ipv4List is not None:
            if IHost.providedBy(intfc.__context__):
                host = intfc.__context__
            else:
                host = intfc.__context__.__parent__
            net = host.__parent__
            for ipv4 in intfc.ipv4List:
                if not net.containsIp(ipv4):
                    raise Invalid("The IP address %s is not in ip-range %s of the "\
                                  "network '%s'" % (ipv4, net.ipv4, net.ikName))

    @invariant
    def ensureMyIpNotAlreadyUsed(intfc):
        if intfc.netType == 'ethernet' and \
             intfc.__context__ is not None and \
           intfc.ipv4List is not None:
            my_catalog = zapi.getUtility(ICatalog)
            alreadyFound = []
            # new Object
            if IHost.providedBy(intfc.__context__):
                for obj in my_catalog.searchResults(\
                    interface_ip_index=convertIpV4(intfc.ipv4List)):
                    ifHost = obj.__parent__
                    ifString = u"%s/%s" % (ifHost.ikName, obj.ikName)
                    alreadyFound.append(ifString)
            # edit Object
            if IInterface.providedBy(intfc.__context__):
                for obj in my_catalog.searchResults(\
                    interface_ip_index=convertIpV4(intfc.ipv4List)):
                    # don't check object itself
                    if obj.objectID != intfc.__context__.objectID:
                        ifHost = obj.__parent__
                        ifString = u"%s/%s" % (ifHost.ikName, obj.ikName)
                        alreadyFound.append(ifString)
            if len(alreadyFound) > 0:
                raise Invalid("The IP address already used in interface %s" % \
                              " ".join(alreadyFound))

class IInterfaceSnmpScanWizard(Interface):
    """A interface object."""
    searchIpV4 = HostIpValid(
            min_length=1,
            max_length=30,
            title=_("IP address"),
            default=u"127.0.0.1",
            required=True)
    indexType = Choice(
        title = _("Index type"),
        vocabulary="SnmpIndexTypes",
        default = u"mac",
        required = True)
