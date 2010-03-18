# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of OperatingSoftware"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.osoftware.interfaces import \
    IOperatingSoftware, IAddOperatingSoftware, IOperatingSoftwareFolder
from org.ict_ok.components.osoftware.osoftware import OperatingSoftware
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.superclass.browser.superclass import \
    Overview as SuperOverview
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm
from org.ict_ok.components.superclass.browser.superclass import \
    GetterColumn, DateGetterColumn, getStateIcon, raw_cell_formatter, \
    getHealth, getTitle, getModifiedDate, link, getActionBottons, IctGetterColumn

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddOperatingSoftware(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Operating Software')
    viewURL = 'add_osoftware.html'
    weight = 50


class MGlobalAddOperatingSoftware(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Operating Software')
    viewURL = 'add_osoftware.html'
    weight = 50
    folderInterface = IOperatingSoftwareFolder

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
    attrInterface = IOperatingSoftware
    factory = OperatingSoftware
    fields = fieldsForFactory(factory, omit_editfields)

# --------------- forms ------------------------------------


class DetailsOperatingSoftwareForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Operating Software Instance')
    factory = OperatingSoftware
    omitFields = OperatingSoftwareDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddOperatingSoftwareForm(AddComponentForm):
    """Add Operating Software Instance form"""
    label = _(u'Add Operating Software Instance')
    factory = OperatingSoftware
    omitFields = OperatingSoftwareDetails.omit_addfields
    attrInterface = IOperatingSoftware
    addInterface = IAddOperatingSoftware
    _session_key = 'org.ict_ok.components.osoftware'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditOperatingSoftwareForm(EditForm):
    """ Edit for Operating Software Instance """
    label = _(u'Operating Software Instance Edit Form')
    factory = OperatingSoftware
    omitFields = OperatingSoftwareDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteOperatingSoftwareForm(DeleteForm):
    """ Delete the Operating Software Instance """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this OperatingSoftware: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IOperatingSoftware
    factory = OperatingSoftware
    factoryId = u'org.ict_ok.components.osoftware.osoftware.OperatingSoftware'
    allFields = fieldsForInterface(attrInterface, [])


class Overview(SuperOverview):
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Health'),
                     getter=getHealth),
        IctGetterColumn(title=_('Title'),
                        getter=getTitle,
                        cell_formatter=link('overview.html')),
        IctGetterColumn(title=_('Device'),
                        getter=lambda i,f: i.device,
                        cell_formatter=link('details.html')),
        DateGetterColumn(title=_('Modified'),
                        getter=getModifiedDate,
                        subsort=True,
                        cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    pos_column_index = 1
    sort_columns = [1, 2, 3, 4, 5]
