# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of OperatingSoftware"""

__version__ = "$Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.components.osoftware.interfaces import IOperatingSoftware, IAddOperatingSoftware
from org.ict_ok.components.osoftware.osoftware import OperatingSoftware
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddOperatingSoftware(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Operating Software')
    viewURL = 'add_osoftware.html'

    weight = 50

# --------------- object details ---------------------------


class OperatingSoftwareDetails(ComponentDetails):
    """ Class for OperatingSoftware details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class OperatingSoftwareFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    fields = field.Fields(IOperatingSoftware).omit(*OperatingSoftwareDetails.omit_viewfields)
    attrInterface = IOperatingSoftware

# --------------- forms ------------------------------------


class DetailsOperatingSoftwareForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Operating Software Instance')
    fields = field.Fields(IOperatingSoftware).omit(*OperatingSoftwareDetails.omit_viewfields)


class AddOperatingSoftwareForm(AddComponentForm):
    """Add Operating Software Instance form"""
    label = _(u'Add Operating Software Instance')
    addFields = field.Fields(IAddOperatingSoftware)
    allFields = field.Fields(IOperatingSoftware).omit(*OperatingSoftwareDetails.omit_addfields)
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget
    factory = OperatingSoftware
    attrInterface = IOperatingSoftware
    _session_key = 'org.ict_ok.components.osoftware'


class EditOperatingSoftwareForm(EditForm):
    """ Edit for Operating Software Instance """
    label = _(u'Operating Software Instance Edit Form')
    fields = field.Fields(IOperatingSoftware).omit(*OperatingSoftwareDetails.omit_editfields)


class DeleteOperatingSoftwareForm(DeleteForm):
    """ Delete the Operating Software Instance """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this OperatingSoftware: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    allFields = field.Fields(IOperatingSoftware)
#    allFields['isTemplate'].widgetFactory = \
#        checkbox.SingleCheckBoxFieldWidget
    attrInterface = IOperatingSoftware
    factory = OperatingSoftware
    factoryId = u'org.ict_ok.components.osoftware.osoftware.OperatingSoftware'
