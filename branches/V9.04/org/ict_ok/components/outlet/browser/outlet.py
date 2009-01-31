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
"""implementation of browser class of Outlet"""

__version__ = "$Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.components.outlet.interfaces import IOutlet, IAddOutlet
from org.ict_ok.components.outlet.outlet import Outlet
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


class MSubAddOutlet(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add an network outlet')
    viewURL = 'add_outlet.html'

    weight = 50

# --------------- object details ---------------------------


class OutletDetails(ComponentDetails):
    """ Class for Outlet details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class OutletFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    fields = field.Fields(IOutlet).omit(*OutletDetails.omit_viewfields)
    attrInterface = IOutlet

# --------------- forms ------------------------------------


class DetailsOutletForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of An network outlet instance')
    fields = field.Fields(IOutlet).omit(*OutletDetails.omit_viewfields)


#class AddOutletForm(AddForm):
#    """Add An network outlet instance form"""
#    label = _(u'Add An network outlet instance')
#    fields = field.Fields(IOutlet).omit(*OutletDetails.omit_addfields) 
#    factory = Outlet
    
    
class AddOutletForm(AddComponentForm):
    label = _(u'Add An network outlet instance')
    addFields = field.Fields(IAddOutlet)
    allFields = field.Fields(IOutlet).omit(*OutletDetails.omit_addfields)
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget
    factory = Outlet
    attrInterface = IOutlet
    _session_key = 'org.ict_ok.components.outlet'


class EditOutletForm(EditForm):
    """ Edit for An network outlet instance """
    label = _(u'An network outlet instance Edit Form')
    fields = field.Fields(IOutlet).omit(*OutletDetails.omit_editfields)
    fields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class DeleteOutletForm(DeleteForm):
    """ Delete the An network outlet instance """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Outlet: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    allFields = field.Fields(IOutlet)
    attrInterface = IOutlet
    factory = Outlet
    factoryId = u'org.ict_ok.components.outlet.outlet.Outlet'
