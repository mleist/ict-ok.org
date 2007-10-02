# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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
import zope.event
from zope.proxy import removeAllProxies
from zope.i18nmessageid import MessageFactory
from zope.lifecycleevent import Attributes, ObjectModifiedEvent

# z3c imports
from z3c.form import form, field

# ict_ok.org imports
from org.ict_ok.components.host.interfaces import IHost, IEventIfEventHost
from org.ict_ok.components.host.host import Host
from org.ict_ok.components.supernode.browser.supernode import SupernodeDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.components.superclass.browser.superclass import applyChanges
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditContent, EditForm
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEvent
from org.ict_ok.components.superclass.interfaces import \
     IEventIfSuperclass

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class MSubAddHost(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Host')
    viewURL = 'add_host.html'
    weight = 50

# --------------- object details ---------------------------


class HostDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['osList']
    omit_addfields = SupernodeDetails.omit_addfields + ['osList']
    omit_editfields = SupernodeDetails.omit_editfields + ['osList']
    #omit_viewfields = SupernodeDetails.omit_viewfields + []
    #omit_addfields = SupernodeDetails.omit_addfields + []
    #omit_editfields = SupernodeDetails.omit_editfields + []

    def getHistory(self):
        """
        return List of history entries for the browser
        """
        retList = []
        obj = removeAllProxies(self.context)
        historyList = obj.history
        for entry in historyList:
            tmpList = entry.getList(['date', 'text', 'level', \
                                     'version', 'bgcolor'])
            retList.append(tmpList )
        retList.sort(lambda a, b: cmp(b[0], a[0]))
        return retList
    
    def getWFMC(self):
        """
        return list of Workflows of this object
        """
        from zope.component import queryUtility
        from org.ict_ok.admin_utils.wfmc.interfaces import \
             IAdmUtilWFMC
        
        utilWFMC = queryUtility(IAdmUtilWFMC)
        #print "utilWFMC: %s" % utilWFMC
        
        from org.ict_ok.components.host.wf import pd
        return pd.activities
        #return utilWFMC


# --------------- forms ------------------------------------


class DetailsHostForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of net')
    fields = field.Fields(IHost).omit(*HostDetails.omit_viewfields)


class AddHostForm(AddForm):
    """Add form."""
    label = _(u'Add Host')
    fields = field.Fields(IHost).omit(*HostDetails.omit_addfields)
    factory = Host


class EditHostForm(EditForm):
    """ Edit form for host """
    form.extends(form.EditForm)
    label = _(u'Host Edit Form')
    fields = field.Fields(IHost).omit(*HostDetails.omit_editfields)


class DeleteHostForm(DeleteForm):
    """ Delete the net """
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this net: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class EditEventHostEventIfForm(EditForm):
    """ Edit Event Interface of object """
    label = _(u'host event interfaces form')
    fields = field.Fields(IEventIfEventHost)
    
    def applyChanges(self, data):
        content = self.getContent()
        changes = applyChanges(self, content, data)
        # ``changes`` is a dictionary; if empty, there were no changes
        if changes:
            #import pdb;pdb.set_trace()
            # Construct change-descriptions for the object-modified event
            descriptions = []
            for interface, attrs in changes.items():
                if interface == IAdmUtilEvent:
                    print "##### Event 2 #######"
                elif IEventIfSuperclass.isEqualOrExtendedBy(interface):
                    print "##### Superclass 2 #######"
                names = attrs.keys()
                for attr in attrs:
                    print "attr: %s (I:%s)" % (attr, interface)
                    print "   old: ", attrs[attr]['oldval']
                    print "   new: ", attrs[attr]['newval']
                descriptions.append(Attributes(interface, *names))
            # Send out a detailed object-modified event
            zope.event.notify(ObjectModifiedEvent(content, *descriptions))
        return changes

