# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of PersonalComputer"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.pc.interfaces import \
    IPersonalComputer, IAddPersonalComputer, IPersonalComputerFolder
from org.ict_ok.components.pc.pc import PersonalComputer
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


class MSubAddPersonalComputer(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Personal Computer')
    viewURL = 'add_pc.html'
    weight = 50


class MGlobalAddPersonalComputer(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Personal Computer')
    viewURL = 'add_pc.html'
    weight = 50
    folderInterface = IPersonalComputerFolder

# --------------- object details ---------------------------


class PersonalComputerDetails(ComponentDetails):
    """ Class for PersonalComputer details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class PersonalComputerFolderDetails(ComponentDetails):
    """ Class for PersonalComputer details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IPersonalComputer
    factory = PersonalComputer
    fields = fieldsForFactory(factory, omit_editfields)

# --------------- forms ------------------------------------


class DetailsPersonalComputerForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Personal Computer')
    factory = PersonalComputer
    omitFields = PersonalComputerDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddPersonalComputerForm(AddComponentForm):
    """Add Personal Computer form"""
    label = _(u'Add Personal Computer')
    factory = PersonalComputer
    attrInterface = IPersonalComputer
    addInterface = IAddPersonalComputer
    omitFields = PersonalComputerDetails.omit_addfields
    _session_key = 'org.ict_ok.components.pc'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = checkbox.SingleCheckBoxFieldWidget


class EditPersonalComputerForm(EditForm):
    """ Edit for Personal Computer """
    label = _(u'Personal Computer Edit Form')
    factory = PersonalComputer
    omitFields = PersonalComputerDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeletePersonalComputerForm(DeleteForm):
    """ Delete the Personal Computer """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this PersonalComputer: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IPersonalComputer
    factory = PersonalComputer
    factoryId = u'org.ict_ok.components.pc.pc.PersonalComputer'
    allFields = fieldsForInterface(attrInterface, [])

#def getRoom(item, formatter):
#    if item.device is not None:
#        return item.device.room
#    return None

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
#        IctGetterColumn(title=_('Device'),
#                        getter=lambda i,f: i.device,
#                        cell_formatter=link('details.html')),
#        IctGetterColumn(title=_('Room'),
#                        getter=getRoom,
#                        cell_formatter=link('details.html')),
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
