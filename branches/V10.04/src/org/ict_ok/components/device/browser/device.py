# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Notebook"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.app.intid.interfaces import IIntIds
from zope.app.pagetemplate.urlquote import URLQuote
from zope.app.appsetup import appsetup
from zope.security import checkPermission

# z3c imports

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.browser.component import ComponentDetails

_ = MessageFactory('org.ict_ok')

# --------------- object details ---------------------------


class DeviceDetails(ComponentDetails):
    """ Class for Notebook details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []

    def actions(self):
        """
        gives us the action dict of the object
        """
        try:
            objId = getUtility(IIntIds).getId(self.context)
        except:
            objId = 1000
        retList = []
        if appsetup.getConfigContext().hasFeature('devmode') and \
           checkPermission('org.ict_ok.components.host.Edit', self.context):
            quoter = URLQuote(self.request.getURL())
            tmpDict = {}
            tmpDict['oid'] = u"c%strigger_online" % objId
            tmpDict['title'] = _(u"Trigger online")
            tmpDict['href'] = u"%s/@@trigger_online?nextURL=%s" % \
                   (zapi.absoluteURL(self.context, self.request),
                    quoter.quote())
            retList.append(tmpDict)
            tmpDict = {}
            tmpDict['oid'] = u"c%strigger_offline" % objId
            tmpDict['title'] = _(u"Trigger offline")
            tmpDict['href'] = u"%s/@@trigger_offline?nextURL=%s" % \
                   (zapi.absoluteURL(self.context, self.request),
                    quoter.quote())
            retList.append(tmpDict)
            tmpDict = {}
            tmpDict['oid'] = u"c%strigger_not1" % objId
            tmpDict['title'] = _(u"Trigger notification1")
            tmpDict['href'] = u"%s/@@trigger_not1?nextURL=%s" % \
                   (zapi.absoluteURL(self.context, self.request),
                    quoter.quote())
            retList.append(tmpDict)
        return retList

    def state(self):
        """
        gives us the state dict of the object
        """
        return IState(self.context).getStateDict()

    def trigger_online(self):
        """
        trigger workflow
        """
#        print "trigger_online@browser"
        self.context.trigger_online()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def trigger_offline(self):
        """
        trigger workflow
        """
#        print "trigger_offline@browser"
        self.context.trigger_offline()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def trigger_not1(self):
        """
        trigger workflow
        """
#        print "trigger_not1@browser"
        self.context.trigger_not1()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')


class DeviceFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']



