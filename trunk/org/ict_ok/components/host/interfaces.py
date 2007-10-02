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
from zope.interface import Attribute
from zope.schema import Bool, Choice, List, Password, Set, TextLine
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

    hostGroup = Set(
        title = _("host groups"),
        value_type = Choice(
            title = _("host"),
            vocabulary="AllHostGroups"),
        default = set([]),
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

    building = TextLine(
        max_length = 80,
        title = _("Building"),
        description = _("The Building."),
        default = u"",
        required = False)

    room = TextLine(
        max_length = 80,
        title = _("Room"),
        description = _("The Room Description."),
        default = u"",
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
        default = True,
        required = False)

    # TODO move to own Interface towards admin_util.esx...
    esxUuid = TextLine(
        max_length = 80,
        title = _("ESX UUID"),
        description = _("UUID of virtual machine in ESX."),
        default = u"",
        required = False)

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
    
    def eventInp_shutdown(self):
        """ start the shutdown of the host """
