# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <i_am@not-there.org>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Group"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.group.interfaces import \
    IGroup, IAddGroup, IGroupFolder
from org.ict_ok.components.group.group import Group
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddGroup(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Group')
    viewURL = 'add_group.html'
    weight = 50


class MGlobalAddGroup(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Group')
    viewURL = 'add_group.html'
    weight = 50
    folderInterface = IGroupFolder

# --------------- object details ---------------------------


class GroupDetails(ComponentDetails):
    """ Class for Group details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class GroupFolderDetails(ComponentDetails):
    """ Class for Group details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IGroup
    factory = Group
    omitFields = GroupDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsGroupForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Group')
    factory = Group
    omitFields = GroupDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddGroupForm(AddComponentForm):
    """Add Group form"""
    label = _(u'Add Group')
    factory = Group
    attrInterface = IGroup
    addInterface = IAddGroup
    omitFields = GroupDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.group'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditGroupForm(EditForm):
    """ Edit for Group """
    label = _(u'Group Edit Form')
    factory = Group
    omitFields = GroupDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteGroupForm(DeleteForm):
    """ Delete the Group """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Group: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = Group
    attrInterface = IGroup
    omitFields = GroupDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.group.group.Group'
    allFields = fieldsForInterface(attrInterface, [])
