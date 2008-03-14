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
"""Interface to jabber notifier"""

__version__ = "$Id$"

# zope imports
from zope.interface import Attribute
from zope.schema import Datetime, Int, Password, TextLine
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.admin_utils.notifier.interfaces import \
     INotifier
from org.ict_ok.schema.ipvalid import HostIpValid

_ = MessageFactory('org.ict_ok')

class INotifierJabber(INotifier):
    """
    component for notifying with jabber
    """
    #enableConnector = Bool(
        #title = _("Connector enabled"),
        #description = _("jabber connector is enabled"),
        #default = False,
        #required = False)

    ipv4Connector = HostIpValid(
        min_length = 1,
        max_length = 30,
        title = _("Connector IP"),
        description = _("IP address of the jabber connector."),
        default = u"127.0.0.1",
        readonly = False,
        required = False)

    portConnector = Int(
        min = 0,
        max = 65535,
        title = _("Connector Port"),
        description = _("Port of the jabber connector"),
        default = 8551,
        required = False)
    
    hostnameServer = TextLine(
        max_length = 80,
        title = _("Jabber servername"),
        description = _("Servername or IP of im server"),
        default = u"jabber.org",
        required = False)

    portServer = Int(
        min = 0,
        max = 65535,
        title = _("Jabber serverport"),
        description = _("Port of the im server"),
        default = 5222,
        required = False)

    authname = TextLine(
        max_length = 80,
        title = _("Username"),
        description = _("Username for im-login"),
        default = u"",
        required = False)

    authpasswd = Password(
        max_length = 80,
        title = _("Password"),
        description = _("Password for im-login"),
        default = u"",
        required = False)

    lastSeenConnector = Datetime(
        title=_("last seen Connector"),
        description=_("Time since last contact with the jabber connector"),
        required=False)

    connectorType = Attribute("Connector Type")
    connectorVersion = Attribute("Connector Version")
    enableConnector = Attribute("Connector enabled")

    def getObjectId(self):
        """
        get 'Universe ID' of object
        returns str
        """

    def sendNotify(self, notifyEvent=None, notifyObj=None):
        """ sending the real notification to the user
        """


    def start_connector(self):
        """ connects to the configured jabber-system
        """

    def stop_connector(self):
        """ disconnects to the configured jabber-system
        """

    def get_isUp(self):
        """ ask for an existing jabber-connector
        """
        
    def connect_server(self):
        """ connect the xmlrpc-agent with the jabber-server
        """
 
    def send_test(self):
        """ send a test message to an existing jabber-server
        """
