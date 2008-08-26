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
import zope.component
from zope.i18nmessageid import MessageFactory
from zope.formlib.form import Fields, FormBase, haveInputWidgets
from zope.formlib.form import action, applyChanges, setUpEditWidgets
from zope.formlib.namedtemplate import NamedTemplate
from zope.formlib.namedtemplate import NamedTemplateImplementation
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.traversing.browser import absoluteURL

from zope.formlib.form import Fields, FormBase, haveInputWidgets
from zope.formlib.form import action, applyChanges, setUpEditWidgets
from zope.pagetemplate.interfaces import IPageTemplate

# z3c imports
from z3c.form import button, field, form
from z3c.form import interfaces
from z3c.formui import layout
from z3c.template import template as z3ctemplate

# ict_ok.org imports
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditContent, EditForm
from org.ict_ok.admin_utils.usermanagement.interfaces import \
     IAdmUtilUserProperties, IAdmUtilUserManagement
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     AdmUtilUserProperties

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


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


class AdmUtilUserManagementDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['objectID']
    omit_editfields = SupernodeDetails.omit_editfields + ['objectID', 'ikName']

#class AdmUtilUserPropertiesForm(EditForm):
    #""" Edit form for the object """
    #label = _(u'edit crossbar properties')
    #fields = Fields(IAdmUtilUserProperties).omit(['dashboard_objs'])

#class AdmUtilUserPropertiesForm2(FormBase):
    #""" Form for user properties
    #"""
    #form_fields = Fields(IAdmUtilUserProperties)
    #label = _(u"Edit your user data")
    #template_l = z3ctemplate.getLayoutTemplate(
        #'org.ict_ok.ikadmin_utils.usermanagement.form')
    ##getPageTemplate(
        ##'org.ict_ok.ikadmin_utils.usermanagement.form')
    ##template = NamedTemplate( \
        ##'org.ict_ok.ikadmin_utils.usermanagement.form')
    
    #def setUpWidgets(self, ignore_request=False):
        ##import pdb; pdb.set_trace()
        #self.adapters = {}
        #self.widgets = setUpEditWidgets(
            #self.form_fields, self.prefix, self.request.principal,
            #self.request, adapters=self.adapters,
            #ignore_request=ignore_request
            #)
        
    #@action(_(u"Save"), condition=haveInputWidgets)
    #def handleSaveButton(self, action, data):
        #principal = self.request.principal
        #if applyChanges(principal, self.form_fields, data, self.adapters):
            #self.status = _(u"Changes saved")
        #else:
            #self.status = _(u"No changes")
        #pass
            
    #def render(self):
        #import pdb; pdb.set_trace()
        #if self.template is None:
            #template = zope.component.getMultiAdapter(
                #(self, self.request), IPageTemplate)
            #return template(self)
        #return self.template()

##form_template = NamedTemplateImplementation( 
    ##ViewPageTemplateFile('form1.pt'))


##class AdmUtilUserPropertiesForm(layout.FormLayoutSupport, form.EditForm):
    ##""" Edit for for site """
    ##label = _(u'edit user properties')
    ##fields = field.Fields(IAdmUtilUserProperties)
    ###fields = field.Fields(AdmUtilUserProperties) #.omit(*SiteDetails.omit_editfields)
    
    ##def updateWidgets(self):
        ##import pdb; pdb.set_trace()
        ##'''See interfaces.IForm'''
        ###def getMultiAdapter(objects, interface=Interface, name=u'', context=None):
        ###self.widgets = zope.component.getMultiAdapter(
            ###(self, self.request, self.getContent()), interfaces.IWidgets)
        ##self.widgets = zope.component.getMultiAdapter(
            ##(self, self.request, AdmUtilUserProperties), interfaces.IWidgets).items()
        ##self.widgets.mode = self.mode
        ##self.widgets.ignoreContext = self.ignoreContext
        ##self.widgets.ignoreRequest = self.ignoreRequest
        ##self.widgets.ignoreReadonly = self.ignoreReadonly
        ##self.widgets.update()
        
    ##def render(self):
        ##'''See interfaces.IForm'''
        ##import pdb; pdb.set_trace()
        ### render content template
        ##if self.template is None:
            ##template = zope.component.getMultiAdapter((self, self.request),
                ##IPageTemplate)
            ##return template(self)
        ##return self.template()

    ##def setUpWidgets(self, ignore_request=False):
        ##self.adapters = {}
        ##self.widgets = setUpEditWidgets(
            ##self.form_fields, self.prefix, self.request.principal,
            ##self.request, adapters=self.adapters,
            ##ignore_request=ignore_request
            ##)

    ##@action(_(u"Save"), condition=haveInputWidgets)
    ##def handleSaveButton(self, action, data):
        ##principal = self.request.principal
        ##if applyChanges(principal, self.form_fields, data, self.adapters):
            ##self.status = _(u"Changes saved")
        ##else:
            ##self.status = _(u"No changes")

##class AdmUtilUserPropertiesForm(FormBase):
    ##""" Form for user properties
    ##"""
    ##form_fields = Fields(IAdmUtilUserProperties)
    ##label = _(u"Edit your user data")
    ##template = NamedTemplate(\
        ##'org.ict_ok.admin_utils.userproperties.form')
    
    ##def setUpWidgets(self, ignore_request=False):
        ##self.adapters = {}
        ##self.widgets = setUpEditWidgets(
            ##self.form_fields, self.prefix, self.request.principal,
            ##self.request, adapters=self.adapters,
            ##ignore_request=ignore_request
            ##)
    ##def setUpEditWidgets(form_fields, form_prefix, context, request,
                         ##adapters=None, for_display=False,
                         ##ignore_request=False):
        
    ##@action(_(u"Save"), condition=haveInputWidgets)
    ##def handleSaveButton(self, action, data):
        ##principal = self.request.principal
        ##if applyChanges(principal, self.form_fields, data, self.adapters):
            ##self.status = _(u"Changes saved")
        ##else:
            ##self.status = _(u"No changes")
            

##form_template = NamedTemplateImplementation(
    ##ViewPageTemplateFile('form1.pt'))


# --------------- forms ------------------------------------


class DetailsAdmUtilUserManagementForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of usermanagement')
    fields = field.Fields(IAdmUtilUserManagement).omit(\
        *AdmUtilUserManagementDetails.omit_viewfields)


class EditAdmUtilUserManagementForm(EditForm):
    """ Edit for for net """
    label = _(u'edit user management')
    fields = field.Fields(IAdmUtilUserManagement).omit(\
        *AdmUtilUserManagementDetails.omit_editfields)
