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
"""Interface of host object"""

__version__ = "$Id$"

# zope imports
from zope.interface import Attribute
from zope.schema import Bool, Choice, List, Password, Set, TextLine, Int
from zope.i18nmessageid import MessageFactory
from zope.app.container.constraints import contains

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.components.supernode.interfaces import \
     IEventIfSupernode

_ = MessageFactory('org.ict_ok')


class IHost(IComponent):
    """A host object."""

    contains('org.ict_ok.components.interface.interfaces.IInterface')

    hostname = TextLine(
        max_length = 80,
        title = _("Hostname"),
        description = _("Name of the system."),
        default = _("systemname"),
        required = True)

    manufacturer = TextLine(
        max_length = 80,
        title = _("Manufacturer"),
        description = _("Name/Address of the manufacturer."),
        default = u"",
        required = False)

    vendor = TextLine(
        max_length = 80,
        title = _("Vendor"),
        description = _("Name/Address of the vendor."),
        default = u"",
        required = False)

    hostGroups = Set(
        title = _("host groups"),
        value_type = Choice(
            title = _("host"),
            vocabulary="AllHostGroups"),
        default = set([]),
        readonly = False,
        required = True)

    productionState = Choice(
        title = _("Production state"),
        vocabulary="AllHostProductionStates",
        default = 'production',
        readonly = False,
        required = True)

    workinggroup = TextLine(
        max_length = 80,
        title = _("Workinggroup"),
        description = _("Name of the workinggroup."),
        default = u"",
        required = False)

    hardware = TextLine(
        max_length = 80,
        title = _("Hardware"),
        description = _("Hardware of the system."),
        default = u"",
        required = False)

    user = TextLine(
        max_length = 80,
        title = _("User"),
        description = _("User which is working with the system."),
        default = u"",
        required = False)


    inv_id = TextLine(
        max_length = 80,
        title = _("inventory id"),
        description = _("Id of inventory."),
        default = u"",
        required = False)

    room = Choice(
        title = _("Room"),
        description = _("The Room Description."),
        vocabulary="AllRoomsVocab",
        required = False)

    osList = List (
        title = _("operating systems"),
        description = _("list of possible operating systems"),
        value_type = TextLine(
            max_length = 200,
            title = _("Operatingsystem"),
            description = _("The OS Description."),
            default = u"",
            required = False),
        default = [],
        required = False)

    snmpVersion = Choice(
        title = _("SNMP version"),
        vocabulary="SnmpVersions",
        default = u"0", # SNMP V1
        required = False)
    
    snmpPort = Int(
        min = 1,
        max = 65535,
        title = _("SNMP port"),
        default = 161,
        required = False)

    snmpReadCommunity = TextLine(
        max_length = 80,
        title = _("SNMP read community"),
        default = u"public",
        required = False)

    snmpWriteCommunity = TextLine(
        max_length = 80,
        title = _("SNMP write community"),
        default = u"private",
        required = False)

    url = TextLine(
        max_length = 80,
        title = _("URL"),
        description = _("URL of system."),
        default = u"",
        required = False)
        
    url_type = Choice(
        title = _("URL browser type"),
        description = _("Type of browser window"),
        default = "direct",
        values = ['direct', 'proxy', 'direct extern', 'proxy extern'],
        required = True)

    url_authname = TextLine(
        max_length = 80,
        title = _("URL Username"),
        description = _("Username for url-browser login"),
        default = u"",
        required = False)

    url_authpasswd = Password(
        max_length = 80,
        title = _("URL Password"),
        description = _("Password for url-browser login"),
        default = u"",
        required = False)

    console = TextLine(
        max_length = 80,
        title = _("Console"),
        description = _("Console of system."),
        default = u"",
        required = False)

    genNagios = Bool(
        title = _("for Nagios"),
        description = _("enabled in Nagios"),
        default = False,
        required = False)

    def trigger_online():
        """
        trigger workflow
        """

    def trigger_offline():
        """
        trigger workflow
        """

    def trigger_not1():
        """
        trigger workflow
        """
        
    def getIpList():
        """ get a list of all possible ips
        """

class IEventIfEventHost(IEventIfSupernode):
    """ event interface of object """
    
    eventInpObjs_shutdown = Set(
        title = _("shutdown event <-"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)

    eventOutObjs_nagiosError = Set(
        title = _("nagiosError ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = False)

    def eventInp_shutdown(eventMsg):
        """ start the shutdown of the host """
