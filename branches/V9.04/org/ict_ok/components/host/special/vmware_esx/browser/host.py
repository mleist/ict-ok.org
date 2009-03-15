# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
#
"""implementation of browser class of Host object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.security import checkPermission
from zope.app.intid.interfaces import IIntIds
from zope.app.pagetemplate.urlquote import URLQuote
from zope.app.appsetup import appsetup

# z3c imports
from z3c.form import form, field

# ict_ok.org imports
from org.ict_ok.components.host.special.vmware_esx.interfaces import \
     IHostVMwareEsx, IEventIfHostVMwareEsx
from org.ict_ok.components.host.special.vmware_esx.host import Host
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.components.host.browser.host import \
     HostDetails as SuperHostDetails
from org.ict_ok.components.host.browser.host import \
     EditEventHostEventIfForm as SuperEditEventIfForm

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class MSubAddHost(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add VMware ESX Server')
    viewURL = 'add_host_vmware_esx.html'
    weight = 50

# --------------- object details ---------------------------


class HostDetails(SuperHostDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SuperHostDetails.omit_viewfields + []
    omit_addfields = SuperHostDetails.omit_addfields + []
    omit_editfields = SuperHostDetails.omit_editfields + []
    
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
            tmpDict['oid'] = u"c%sshutdownHost" % objId
            tmpDict['title'] = _(u"shutdown host")
            tmpDict['href'] = u"%s/@@shutdownHost.html?nextURL=%s" % \
                   (zapi.absoluteURL(self.context, self.request),
                    quoter.quote())
            retList.append(tmpDict)
            tmpDict = {}
            tmpDict['oid'] = u"c%senterMaintenanceMode" % objId
            tmpDict['title'] = _(u"enter maintenance mode")
            tmpDict['href'] = u"%s/@@enterMaintenanceMode.html?nextURL=%s" % \
                   (zapi.absoluteURL(self.context, self.request),
                    quoter.quote())
            retList.append(tmpDict)
        return SuperHostDetails.actions(self) + retList

    def shutdownHost(self):
        """
        trigger shutdownHost
        """
        print "shutdownHost@browser"
        self.context.shutdownHost()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def enterMaintenanceMode(self):
        """
        trigger enterMaintenanceMode
        """
        print "enterMaintenanceMode@browser"
        self.context.enterMaintenanceMode()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

# --------------- forms ------------------------------------


class DetailsHostForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of VMware ESX Server')
    fields = field.Fields(IHostVMwareEsx).omit(*HostDetails.omit_viewfields)


class AddHostForm(AddForm):
    """Add form."""
    label = _(u'Add VMware ESX Server')
    fields = field.Fields(IHostVMwareEsx).omit(*HostDetails.omit_addfields)
    factory = Host


class EditHostForm(EditForm):
    """ Edit form for host """
    form.extends(form.EditForm)
    label = _(u'VMware ESX Server Edit Form')
    fields = field.Fields(IHostVMwareEsx).omit(*HostDetails.omit_editfields)


class EditEventHostEventIfForm(SuperEditEventIfForm):
    """ Edit Event Interface of object """
    label = _(u'esx host event interfaces form')
    fields = field.Fields(IEventIfHostVMwareEsx)
    
