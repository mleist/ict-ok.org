# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0621,W0611,W0232,W0201,W0142
#
"""implementation of browser class of usermanagement handler
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from zope.app import zapi

# z3c imports
from z3c.form import field
from z3c.form import interfaces

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditContent, EditForm
from org.ict_ok.admin_utils.usermanagement.interfaces import \
     IAdmUtilUserProperties, IAdmUtilUserManagement, IEditPassword, \
     IAdmUtilUserPreferences
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     AdmUtilUserManagement, AdmUtilUserProperties
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor

_ = MessageFactory('org.ict_ok')


# --------------- helper functions -------------------------

def applyPasswdChanges(form, content, data):
    # copied from z3c.form.form
    changes = {}
    if data['password1'] != data['password2']:
        raise interfaces.WidgetActionExecutionError(\
            'password1', 
            zope.interface.Invalid("passwords aren't equal"))
    reqPrincipal = form.request.principal
    (prefix, id) = reqPrincipal.id.split('.')
    utilUserMagagement = getUtility(IAdmUtilUserManagement)
    principalFolder = utilUserMagagement[u'principals']
    if principalFolder.prefix == prefix+'.':
        intPrincipal = principalFolder.get(id)
        if intPrincipal is None:
            raise interfaces.WidgetActionExecutionError(\
                'password_old', 
                zope.interface.Invalid("error in old password"))
        if intPrincipal.checkPassword(data['password_old']) is False:
            raise interfaces.WidgetActionExecutionError(\
                'password_old', 
                zope.interface.Invalid("error in old password"))
        intPrincipal.setPassword(data['password1'])
        changes.setdefault(IEditPassword, {}).setdefault('password', {})['newval'] = "****"
        changes.setdefault(IEditPassword, {}).setdefault('password', {})['oldval'] = "####"
    return changes


# --------------- menu entries -----------------------------


class MSubPassword(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Change password')
    viewURL = 'password.html'
    weight = 120


class MSubPreferences(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Preferences')
    viewURL = 'preferences.html'
    weight = 100


class MSubAddDashboard(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'[+]')
    viewURL = 'add_dashboard.html'
    weight = 2
    
    def render(self):
        """Return the template with the option 'menus'"""
        userProps = AdmUtilUserProperties(self.request.principal)
        if self.context in userProps.dashboard_objs:
            return
        else:
            return self.template()

class MSubDelDashboard(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'[-]')
    viewURL = 'del_dashboard.html'
    weight = 2

    def render(self):
        """Return the template with the option 'menus'"""
        userProps = AdmUtilUserProperties(self.request.principal)
        if self.context in userProps.dashboard_objs:
            return self.template()
        else:
            return

# --------------- object details ---------------------------

class AdmUtilUserManagementPreferences:
    def preferences(self):
        utilUserMagagement = getUtility(IAdmUtilUserManagement)
        return self.request.response.redirect(\
            zapi.absoluteURL(utilUserMagagement, self.request)+\
            '/@@preferences.html')
    def version(self):
        utilSupervisor = getUtility(IAdmUtilSupervisor)
        return self.request.response.redirect(\
            zapi.absoluteURL(utilSupervisor, self.request)+\
            '/@@version.html')
    def fsearch(self):
        utilSupervisor = getUtility(IAdmUtilSupervisor,
                                    name='AdmUtilSupervisor')
        if self.request.has_key('QUERY_STRING'):
            queryString = '?%s' % self.request['QUERY_STRING']
        else:
            queryString =''
        return self.request.response.redirect(\
            zapi.absoluteURL(utilSupervisor, self.request)+\
            '/@@fsearch.html%s' % queryString)


class AdmUtilUserManagementDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + \
        ['objectID', 'ikName', 'ikNotes', 'ikComment']
    omit_editfields = SupernodeDetails.omit_editfields + \
        ['objectID', 'ikName', 'ikNotes', 'ikComment']

# --------------- forms ------------------------------------


class DetailsAdmUtilUserManagementForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of usermanagement')
    factory = AdmUtilUserManagement
    omitFields = AdmUtilUserManagementDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)




class EditAdmUtilUserManagementForm(EditForm):
    """ Edit for for net """
    label = _(u'edit user settings')
    fields = field.Fields(IAdmUtilUserManagement).omit(\
        *AdmUtilUserManagementDetails.omit_editfields)


class EditAdmUtilUserManagementForm(EditForm):
    """ Edit for for net """
    label = _(u'edit user settings')
    factory = AdmUtilUserManagement
    omitFields = AdmUtilUserManagementDetails.omit_editfields
    fields = field.Fields(IAdmUtilUserManagement).omit(\
        *omitFields)
#    fields = fieldsForFactory(factory, omitFields)


class PreferencesAdmUtilUserManagementForm(EditForm):
    """ Edit for for net """
    label = _(u'edit user settings')
    factory = AdmUtilUserManagement
    omitFields = AdmUtilUserManagementDetails.omit_editfields
    fields = fieldsForInterface(IAdmUtilUserPreferences, omitFields)



class EditPasswordForm(EditForm):
    """ Edit for for net """
    label = _(u'edit user password')
    fields = field.Fields(IEditPassword)

    def applyChanges(self, data):
        content = self.getContent()
        changes = applyPasswdChanges(self, content, data)
        # ``changes`` is a dictionary; if empty, there were no changes
        if changes:
            # Construct change-descriptions for the object-modified event
            descriptions = []
            for interface, names in changes.items():
                descriptions.append(
                    zope.lifecycleevent.Attributes(interface, *names))
            # Send out a detailed object-modified event
            zope.event.notify(
                zope.lifecycleevent.ObjectModifiedEvent(content, *descriptions))
        return changes
