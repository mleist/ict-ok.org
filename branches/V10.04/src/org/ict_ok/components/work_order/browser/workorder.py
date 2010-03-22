# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of WorkOrder"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.workorder.interfaces import IWorkOrder, IAddWorkOrder
from org.ict_ok.components.workorder.workorder import WorkOrder
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddWorkOrder(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Work order')
    viewURL = 'add_workorder.html'

    weight = 50

# --------------- object details ---------------------------


class WorkOrderDetails(ComponentDetails):
    """ Class for WorkOrder details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class WorkOrderFolderDetails(ComponentDetails):
    """ Class for WorkOrder details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IWorkOrder
    factory = WorkOrder
    omitFields = WorkOrderDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsWorkOrderForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Work order')
    factory = WorkOrder
    omitFields = WorkOrderDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddWorkOrderForm(AddComponentForm):
    """Add Work order form"""
    label = _(u'Add Work order')
    factory = WorkOrder
    attrInterface = IWorkOrder
    addInterface = IAddWorkOrder
    omitFields = WorkOrderDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.workorder'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditWorkOrderForm(EditForm):
    """ Edit for Work order """
    label = _(u'Work order Edit Form')
    factory = WorkOrder
    omitFields = WorkOrderDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteWorkOrderForm(DeleteForm):
    """ Delete the Work order """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this WorkOrder: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = WorkOrder
    attrInterface = IWorkOrder
    omitFields = WorkOrderDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.workorder.workorder.WorkOrder'
    allFields = fieldsForInterface(attrInterface, [])
