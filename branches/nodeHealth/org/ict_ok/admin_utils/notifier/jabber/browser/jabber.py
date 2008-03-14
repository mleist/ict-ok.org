# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0232,W0142,R0901
#
"""implementation of browser class of jabber-generator
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.security import checkPermission
from zope.app.pagetemplate.urlquote import URLQuote

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.notifier.jabber.interfaces import \
     INotifierJabber

_ = MessageFactory('org.ict_ok')

class NotifierJabberDetails(SupernodeDetails):
    """
    Browser details for jabber-connector
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_editfields = SupernodeDetails.omit_editfields + []
    def actions(self):
        """
        gives us the action dict of the object
        """
        retList = []
        if checkPermission('org.ict_ok.admin_utils.notifier.Edit',
                           self.context):
            quoter = URLQuote(self.request.getURL())
            if self.context.enableConnector:
                tmpDict = {}
                #tmpDict['oid'] = u"c%s" % objId
                tmpDict['oid'] = u"c000stop_connector"
                tmpDict['title'] = _(u"stop jabber-connector")
                tmpDict['href'] = u"%s/@@stop_connector?nextURL=%s" % \
                       (zapi.getPath(self.context),
                        quoter.quote())
                tmpDict['tooltip'] = _(u"stops the jabber-connector (as user:%s)"\
                                       % self.request.principal.title)
                retList.append(tmpDict)
                tmpDict = {}
                tmpDict['oid'] = u"c000get_isup"
                tmpDict['title'] = _(u"is jabber-connector up")
                tmpDict['href'] = u"%s/@@get_isup?nextURL=%s" % \
                       (zapi.getPath(self.context),
                        quoter.quote())
                tmpDict['tooltip'] = _(u"ask the jabber-connector for watchdog")
                retList.append(tmpDict)
                tmpDict = {}
                tmpDict['oid'] = u"c000send_test"
                tmpDict['title'] = _(u"send test message")
                tmpDict['href'] = u"%s/@@send_test?nextURL=%s" % \
                       (zapi.getPath(self.context),
                        quoter.quote())
                tmpDict['tooltip'] = _(u"send test message to im-server")
                retList.append(tmpDict)
            else:
                tmpDict = {}
                #tmpDict['oid'] = u"c%s" % objId
                tmpDict['oid'] = u"c000start_connector"
                tmpDict['title'] = _(u"start jabber-connector")
                tmpDict['href'] = u"%s/@@start_connector?nextURL=%s" % \
                       (zapi.getPath(self.context),
                        quoter.quote())
                tmpDict['tooltip'] = _(u"starts the jabber-connector (as user:%s)"\
                                       % self.request.principal.title)
                retList.append(tmpDict)
        #tmpDict = {}
        #tmpDict['oid'] = u"a12345"
        #tmpDict['title'] = u"ich bin ein Titel"
        #tmpDict['href'] = u"http://www.essen.de"
        #tmpDict['tooltip'] = u"ich bin der \"aa\" 'bb' dazugehörige Tooltip Essen"
        #retList.append(tmpDict)
        return retList

    def start_connector(self):
        """
        connects to the configured jabber-system
        """
        print "NotifierJabberDetails::start_connector()"
        self.context.start_connector()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def stop_connector(self):
        """
        disconnects to the configured jabber-system
        """
        print "NotifierJabberDetails::stop_connector()"
        self.context.stop_connector()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def get_isUp(self):
        """
        ask for an existing jabber-connector
        """
        print "NotifierJabberDetails::get_isUp()"
        self.context.get_isUp()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def send_test(self):
        """
        send a test message to an existing jabber-server
        """
        print "NotifierJabberDetails::send_test()"
        self.context.send_test()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def getConfig(self):
        """Trigger configuration by web browser
        """
        return self.context.getConfig()


# --------------- forms ------------------------------------

class ViewNotifierJabberForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of graphviz adapter')
    fields = field.Fields(INotifierJabber).omit(\
        *NotifierJabberDetails.omit_viewfields)


class EditNotifierJabberForm(EditForm):
    """ Edit for for net """
    label = _(u'edit graphviz adapter')
    fields = field.Fields(INotifierJabber).omit(\
        *NotifierJabberDetails.omit_editfields)

