# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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

# phython imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.formlib.form import Fields, FormBase, haveInputWidgets
from zope.formlib.form import action, applyChanges, setUpEditWidgets
from zope.formlib.namedtemplate import NamedTemplate
from zope.formlib.namedtemplate import NamedTemplateImplementation
from zope.app.pagetemplate import ViewPageTemplateFile

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.usermanagement.interfaces import \
     IAdmUtilUserManagement

_ = MessageFactory('org.ict_ok')


class AdmUtilUserManagementDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_editfields = SupernodeDetails.omit_editfields + []

class AdmUtilUserManagementForm(FormBase):
    """ Form for user properties
    """
    form_fields = Fields(IAdmUtilUserManagement)
    label = _(u"Edit your user data")
    template = NamedTemplate(\
        'org.ict_ok.admin_utils.usermanagement.form')
    
    def setUpWidgets(self, ignore_request=False):
        self.adapters = {}
        self.widgets = setUpEditWidgets(
            self.form_fields, self.prefix, self.request.principal,
            self.request, adapters=self.adapters,
            ignore_request=ignore_request
            )
        
    @action(_(u"Save"), condition=haveInputWidgets)
    def handleSaveButton(self, action, data):
        principal = self.request.principal
        if applyChanges(principal, self.form_fields, data, self.adapters):
            self.status = _(u"Changes saved")
        else:
            self.status = _(u"No changes")
            

form_template = NamedTemplateImplementation(
    ViewPageTemplateFile('form1.pt'))


# --------------- forms ------------------------------------


class ViewAdmUtilUserManagementForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of graphviz adapter')
    fields = field.Fields(IAdmUtilUserManagement).omit(\
        *AdmUtilUserManagementDetails.omit_viewfields)


class EditAdmUtilUserManagementForm(EditForm):
    """ Edit for for net """
    label = _(u'edit graphviz adapter')
    fields = field.Fields(IAdmUtilUserManagement).omit(\
        *AdmUtilUserManagementDetails.omit_editfields)
