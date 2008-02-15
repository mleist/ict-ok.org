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

# phython imports

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from zope.security import checkPermission
from zope.app.intid.interfaces import IIntIds
from zope.app.pagetemplate.urlquote import URLQuote
from zope.app.appsetup import appsetup

# z3c imports
from z3c.form import form, field

# ict_ok.org imports
from org.ict_ok.components.host.special.vmware_vm.interfaces import \
     IHostVMwareVm
from org.ict_ok.components.host.special.vmware_vm.host import Host
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.components.host.browser.host import \
     HostDetails as SuperHostDetails

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class MSubAddHost(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add VMware Virtual Machine')
    viewURL = 'add_host_vmware_vm.html'
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
            tmpDict['oid'] = u"c%s" % objId
            tmpDict['title'] = _(u"Power off")
            tmpDict['href'] = u"%s/@@poweroff.html?nextURL=%s" % \
                   (zapi.getPath( self.context),
                    quoter.quote())
            retList.append(tmpDict)
            tmpDict = {}
            tmpDict['oid'] = u"c%s" % objId
            tmpDict['title'] = _(u"Power on")
            tmpDict['href'] = u"%s/@@poweron.html?nextURL=%s" % \
                   (zapi.getPath( self.context),
                    quoter.quote())
            retList.append(tmpDict)
        return SuperHostDetails.actions(self) + retList

    def poweroff(self):
        """
        trigger poweroff
        """
        print "poweroff@browser"
        self.context.poweroff()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def poweron(self):
        """
        trigger poweron
        """
        print "poweron@browser"
        self.context.poweron()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

# --------------- forms ------------------------------------



class DetailsHostForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of net')
    fields = field.Fields(IHostVMwareVm).omit(*HostDetails.omit_viewfields)


class AddHostForm(AddForm):
    """Add form."""
    label = _(u'Add VMware Virtual Machine')
    fields = field.Fields(IHostVMwareVm).omit(*HostDetails.omit_addfields)
    factory = Host


class EditHostForm(EditForm):
    """ Edit form for host """
    form.extends(form.EditForm)
    label = _(u'VMware Virtual Machine Edit Form')
    fields = field.Fields(IHostVMwareVm).omit(*HostDetails.omit_editfields)
