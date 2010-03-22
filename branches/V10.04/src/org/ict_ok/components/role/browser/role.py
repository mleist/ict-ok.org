# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Role"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.role.interfaces import \
    IRole, IAddRole, IRoleFolder
from org.ict_ok.components.role.role import Role
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddRole(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Role')
    viewURL = 'add_role.html'
    weight = 50


class MGlobalAddRole(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Role')
    viewURL = 'add_role.html'
    weight = 50
    folderInterface = IRoleFolder

# --------------- object details ---------------------------


class RoleDetails(ComponentDetails):
    """ Class for Role details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class RoleFolderDetails(ComponentDetails):
    """ Class for Role details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IRole
    factory = Role
    omitFields = RoleDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsRoleForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Role')
    factory = Role
    omitFields = RoleDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddRoleForm(AddComponentForm):
    """Add Role form"""
    label = _(u'Add Role')
    factory = Role
    attrInterface = IRole
    addInterface = IAddRole
    omitFields = RoleDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.role'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditRoleForm(EditForm):
    """ Edit for Role """
    label = _(u'Role Edit Form')
    factory = Role
    omitFields = RoleDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteRoleForm(DeleteForm):
    """ Delete the Role """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Role: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = Role
    attrInterface = IRole
    omitFields = RoleDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.role.role.Role'
    allFields = fieldsForInterface(attrInterface, [])
