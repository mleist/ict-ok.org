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
"""implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.i18nmessageid import MessageFactory
import zope.event
from zope.lifecycleevent import Attributes, ObjectModifiedEvent
from zope.app.catalog.interfaces import ICatalog
from zope.security import checkPermission
from zope.app.pagetemplate.urlquote import URLQuote

# zc imports

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEvent
from org.ict_ok.admin_utils.eventcrossbar.event import \
     AdmUtilEvent
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.components.superclass.browser.superclass import applyChanges
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------

class MSubAddEvent(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Event')
    viewURL = 'add_event.html'
    weight = 50


class AdmUtilEventDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_addfields = SupernodeDetails.omit_addfields + ['inpObjects']
    omit_editfields = SupernodeDetails.omit_editfields + ['inpObjects']
    
    def actions(self):
        """
        gives us the action dict of the object
        """
        try:
            objId = getUtility(IIntIds).getId(self.context)
        except KeyError:
            objId = 1000
        retList = []
        if checkPermission('org.ict_ok.admin_utils.event.Send', self.context):
            quoter = URLQuote(self.request.getURL())
            tmpDict = {}
            tmpDict['oid'] = u"c%ssend_event" % objId
            tmpDict['title'] = _(u"send it")
            tmpDict['href'] = u"%s/@@send_event.html?nextURL=%s" % \
                   (zapi.getPath( self.context),
                    quoter.quote())
            tmpDict['tooltip'] = _(u"sends an the event to the list of receivers")
            retList.append(tmpDict)
        return retList
    
    def send_event(self):
        """
        sends an the event to the list of receivers
        """
        self.context.send_event(\
            logText=u"event manually triggered by %s" % \
            self.request.principal.title)
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

# --------------- forms ------------------------------------


class DetailsAdmUtilEventForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Event')
    factory = AdmUtilEvent
    omitFields = AdmUtilEventDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

    def update(self):
        self.context.removeInvalidOidFromInpOutObjects()
        DisplayForm.update(self)


class AddAdmUtilEventForm(AddForm):
    """Add form."""
    label = _(u'add event')
    factory = AdmUtilEvent
    omitFields = AdmUtilEventDetails.omit_addfields
    fields = fieldsForFactory(factory, omitFields)


class EditAdmUtilEventForm(EditForm):
    """ Edit form for the object """
    label = _(u'edit event properties')
    factory = AdmUtilEvent
    omitFields = AdmUtilEventDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)

    def update(self):
        self.context.removeInvalidOidFromInpOutObjects()
        EditForm.update(self)
    def applyChanges(self, data):
        content = self.getContent()
        changes = applyChanges(self, content, data)
        # ``changes`` is a dictionary; if empty, there were no changes
        if changes:
            # Construct change-descriptions for the object-modified event
            descriptions = []
            for interface, attrs in changes.items():
                if interface == IAdmUtilEvent and \
                   'outObjects' in attrs:
                    print "##### Event 3 #######"
                    newSet = attrs['outObjects']['newval']
                    oldSet = attrs['outObjects']['oldval']
                    if type(newSet) == type(set()) and \
                       type(oldSet) == type(set()):
                        newEntries = newSet.difference(oldSet)
                        oldEntries = oldSet.difference(newSet)
                        #print "oldEntries", oldEntries
                        #print "newEntries", newEntries
                        for myString in oldEntries:
                            [oid, funct] = myString.split('.', 2)
                            my_catalog = zapi.getUtility(ICatalog)
                            for resObj in my_catalog.searchResults(oid_index=oid):
                                #print "delete from ", resObj
                                resObj.delFromEventInpObjs(funct, content)
                        for myString in newEntries:
                            [oid, funct] = myString.split('.', 2)
                            my_catalog = zapi.getUtility(ICatalog)
                            for resObj in my_catalog.searchResults(oid_index=oid):
                                #print "add to ", resObj
                                resObj.addToEventInpObjs(funct, content)
                names = attrs.keys()
                #for attr in attrs:
                    #print "attr: %s (I:%s)" % (attr, interface)
                    #print "   old: ", attrs[attr]['oldval']
                    #print "   new: ", attrs[attr]['newval']
                descriptions.append(Attributes(interface, *names))
            # Send out a detailed object-modified event
            zope.event.notify(ObjectModifiedEvent(content, *descriptions))
        return changes
