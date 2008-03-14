# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0602
#
"""Configuration adapter for jabber-config files
"""

__version__ = "$Id$"

# phython imports
import xmlrpclib
import logging
from datetime import datetime
from pytz import timezone

# zope imports
from zope.component import adapter
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

# ict_ok.org imports
from org.ict_ok.admin_utils.notifier.notifier import \
     Notifier
from org.ict_ok.admin_utils.notifier.jabber.interfaces import \
     INotifierJabber
#from org.ict_ok.agents.jabber.ik_ssl_xmlrpc_clnt import MyTransport

logger = logging.getLogger("NotifierJabber")
berlinTZ = timezone('Europe/Berlin')


class NotifierJabber(Notifier):
    """Implementation of jabber notifier wrapper
    """

    implements(INotifierJabber)

    ipv4Connector = FieldProperty(INotifierJabber['ipv4Connector'])
    portConnector = FieldProperty(INotifierJabber['portConnector'])
    hostnameServer = FieldProperty(INotifierJabber['hostnameServer'])
    portServer = FieldProperty(INotifierJabber['portServer'])
    authname = FieldProperty(INotifierJabber['authname'])
    authpasswd = FieldProperty(INotifierJabber['authpasswd'])
    lastSeenConnector = FieldProperty(INotifierJabber['lastSeenConnector'])

    def __init__(self):
        Notifier.__init__(self)
        self.ikRevision = __version__
        self.connectorType = u""
        self.connectorVersion = u""
        self.enableConnector = False
        self.ipv4Connector = u"127.0.0.1"
        self.portConnector = 8551
        self.hostnameServer = u"jabber.org"
        self.portServer = 5222
        self.authname = u""
        self.authpasswd = u""
        self.lastSeenConnector = None

    def sendNotify(self, notifyEvent=None, notifyObj=None):
        """
        sending the real notification to the user
        """
        print "NotifierJabber::sendNotify(%s, %s)" % (notifyEvent, notifyObj)


    def start_connector(self):
        """
        connects to the configured jabber-system
        """
        print "NotifierJabber::start_connector()"
        self.enableConnector = True
        self.get_isUp()
        self.connect_server()

    def stop_connector(self):
        """
        disconnects to the configured jabber-system
        """
        print "NotifierJabber::stop_connector()"
        self.enableConnector = False

    def get_isUp(self):
        """
        ask for an existing jabber-connector
        """
        print "NotifierJabber::get_isUp()"
        if self.enableConnector:
            tmp_url = u"https://%s:%s/" % (self.ipv4Connector,
                                           self.portConnector)
            try:
                tmp_server = xmlrpclib.ServerProxy(tmp_url,
                                                   transport=MyTransport())
                if tmp_server.isUp():
                    self.lastSeenConnector = datetime.now(berlinTZ)
                    #print "lll: %s" % dir(tmp_server)
                    self.connectorType = tmp_server.getType()
                    self.connectorVersion = tmp_server.getVersion()
                    del tmp_server
                    return True
            except xmlrpclib.Error, errText:
                logger.error("XMLRPC-Error: %s" % errText)
                return False
            except Exception, errText:
                logger.error("XMLRPC-Error: %s" % errText)
                return False
        return False

    def connect_server(self):
        """ connect the xmlrpc-agent with the jabber-server
        """
        print "NotifierJabber::connect_server()"
        if self.enableConnector:
            tmp_url = u"https://%s:%s/" % (self.ipv4Connector,
                                           self.portConnector)
            try:
                tmp_server = xmlrpclib.ServerProxy(tmp_url,
                                                   transport=MyTransport())
                retVal = tmp_server.connectServer(self.getObjectId(),
                                                  self.hostnameServer,
                                                  self.portServer,
                                                  self.authname,
                                                  self.authpasswd)
                return retVal
            except xmlrpclib.Error, errText:
                logger.error("XMLRPC-Error: %s" % errText)
                return False
            except Exception, errText:
                logger.error("XMLRPC-Error: %s" % errText)
                return False
        return False
 
    def send_test(self):
        """ send a test message to an existing jabber-server
        """
        print "NotifierJabber::send_test()"
        if self.enableConnector:
            tmp_url = u"https://%s:%s/" % (self.ipv4Connector,
                                           self.portConnector)
            try:
                tmp_server = xmlrpclib.ServerProxy(tmp_url,
                                                   transport=MyTransport())
                retVal = tmp_server.sendTest(self.getObjectId())
                return retVal
            except xmlrpclib.Error, errText:
                logger.error("XMLRPC-Error: %s" % errText)
                return False
            except Exception, errText:
                logger.error("XMLRPC-Error: %s" % errText)
                return False
        return False
 

@adapter(INotifierJabber, IObjectModifiedEvent)
def notifyModifiedEvent(instance, event):
    print "INotifierJabber::notifyModifiedEvent(%s, %s)" % (instance, event)
    print "dir(event): %s" % dir(event)
    if instance.enableConnector:
        #tmp_url = u"https://%s:%s/" % (instance.ipv4Connector,
                                      #instance.portConnector)
        #tmp_server = xmlrpclib.ServerProxy(tmp_url,
                                           #transport=MyTransport())

        print "**** 1a"
        instance.connect_server()
        print "**** 1b"
    else:
        print "**** 2"
    try:
        print "event.descriptions: %s" % (event.descriptions)
        for i in event.descriptions:
            print u"descr: %s" %i
            print u"descr.interface: %s" % str(i.interface)
            for j in i.attributes:
                print u"    attribute / j: %s" % j
                print u"    attribute / type(j): %s" % (type(j))
    except:
        pass
