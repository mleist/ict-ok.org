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
"""implementation of browser class of Room object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.app.catalog.interfaces import ICatalog

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.components.room.interfaces import IRoom, IAddRoom
from org.ict_ok.components.room.room import Room
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.supernode.interfaces import IContentList
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.superclass.browser.superclass import \
     Overview as SuperclassOverview
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddRoom(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Room')
    viewURL = 'add_room.html'
    weight = 50


# --------------- object details ---------------------------


class RoomDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class RoomFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    fields = field.Fields(IRoom).omit(*RoomDetails.omit_viewfields)
    attrInterface = IRoom

# --------------- forms ------------------------------------


class DetailsRoomForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of room')
    fields = field.Fields(IRoom).omit(*RoomDetails.omit_viewfields)


#class AddRoomForm(AddForm):
#    """Add form."""
#    label = _(u'Add Room')
#    fields = field.Fields(IRoom).omit(*RoomDetails.omit_addfields)
#    factory = Room
    

class AddRoomForm(AddComponentForm):
    label = _(u'Add Room')
    addFields = field.Fields(IAddRoom)
    allFields = field.Fields(IRoom).omit(*RoomDetails.omit_addfields)
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget
    factory = Room
    attrInterface = IRoom
    _session_key = 'org.ict_ok.components.room'


class EditRoomForm(EditForm):
    """ Edit for for net """
    label = _(u'Room Edit Form')
    fields = field.Fields(IRoom).omit(*RoomDetails.omit_editfields)
    fields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class DeleteRoomForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this room: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class Overview(SuperclassOverview):
    """Overview Pagelet"""
    def objs(self):
        """List of Content objects"""
        try:
            return IContentList(self.context).getContentList()
        except TypeError:
            return []


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    allFields = field.Fields(IRoom)
    attrInterface = IRoom
    factory = Room
    factoryId = u'org.ict_ok.components.room.room.Room'
