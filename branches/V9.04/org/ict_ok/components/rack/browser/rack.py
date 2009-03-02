# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 411 2009-01-29 16:16:51Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Rack"""

__version__ = "$Id: template.py_cog 411 2009-01-29 16:16:51Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.rack.interfaces import IRack, IAddRack
from org.ict_ok.components.rack.rack import Rack
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


class MSubAddRack(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Device rack')
    viewURL = 'add_rack.html'

    weight = 50

# --------------- object details ---------------------------


class RackDetails(ComponentDetails):
    """ Class for Rack details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class RackFolderDetails(ComponentDetails):
    """ Class for Rack details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    fields = field.Fields(IRack).omit(*RackDetails.omit_viewfields)
    attrInterface = IRack

# --------------- forms ------------------------------------


class DetailsRackForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Device rack')
    factory = Rack
    omitFields = RackDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddRackForm(AddComponentForm):
    """Add Device rack form"""
    label = _(u'Add Device rack')
    factory = Rack
    omitFields = RackDetails.omit_addfields
    attrInterface = IRack
    addInterface = IAddRack
    _session_key = 'org.ict_ok.components.rack'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = checkbox.SingleCheckBoxFieldWidget


class EditRackForm(EditForm):
    """ Edit for Device rack """
    label = _(u'Device rack Edit Form')
    factory = Rack
    omitFields = RackDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteRackForm(DeleteForm):
    """ Delete the Device rack """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Rack: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IRack
    factory = Rack
    factoryId = u'org.ict_ok.components.rack.rack.Rack'
    allFields = fieldsForInterface(attrInterface, [])
