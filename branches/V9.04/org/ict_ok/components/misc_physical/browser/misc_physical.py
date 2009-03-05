# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 467 2009-03-05 04:28:59Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of MiscPhysical"""

__version__ = "$Id: template.py_cog 467 2009-03-05 04:28:59Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.component import queryUtility
from zope.app.intid.interfaces import IIntIds

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.misc_physical.interfaces import IMiscPhysical, IAddMiscPhysical
from org.ict_ok.components.misc_physical.misc_physical import MiscPhysical
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.superclass.browser.superclass import \
    Overview as SuperOverview
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm
from org.ict_ok.components.superclass.browser.superclass import \
    GetterColumn, DateGetterColumn, getStateIcon, raw_cell_formatter, \
    getHealth, getTitle, getModifiedDate, link, getActionBottons, IctGetterColumn
from org.ict_ok.components.physical_component.browser.physical_component import \
    getUserName, fsearch_user_formatter
from org.ict_ok.components.physical_component.browser.physical_component import \
    PhysicalComponentDetails
from org.ict_ok.osi.interfaces import IOSIModel
from org.ict_ok.osi.interfaces import IPhysicalLayer

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddMiscPhysical(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add miscellaneous physical component')
    viewURL = 'add_misc_physical.html'

    weight = 50


class MSubInvMiscPhysical(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All miscellaneous physical components')
    viewURL = '/@@all_misc_physicals.html'
    weight = 100

# --------------- object details ---------------------------


class MiscPhysicalDetails(PhysicalComponentDetails):
    """ Class for MiscPhysical details
    """
    omit_viewfields = PhysicalComponentDetails.omit_viewfields + []
    omit_addfields = PhysicalComponentDetails.omit_addfields + []
    omit_editfields = PhysicalComponentDetails.omit_editfields + []


class MiscPhysicalFolderDetails(ComponentDetails):
    """ Class for MiscPhysical details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IMiscPhysical
    factory = MiscPhysical
    omitFields = MiscPhysicalDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsMiscPhysicalForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of miscellaneous physical component')
    factory = MiscPhysical
    omitFields = MiscPhysicalDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddMiscPhysicalForm(AddComponentForm):
    """Add miscellaneous physical component form"""
    label = _(u'Add miscellaneous physical component')
    factory = MiscPhysical
    attrInterface = IMiscPhysical
    addInterface = IAddMiscPhysical
    omitFields = MiscPhysicalDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.misc_physical'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditMiscPhysicalForm(EditForm):
    """ Edit for miscellaneous physical component """
    label = _(u'miscellaneous physical component Edit Form')
    factory = MiscPhysical
    omitFields = MiscPhysicalDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteMiscPhysicalForm(DeleteForm):
    """ Delete the miscellaneous physical component """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this MiscPhysical: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = MiscPhysical
    attrInterface = IMiscPhysical
    omitFields = MiscPhysicalDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.misc_physical.misc_physical.MiscPhysical'
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
        IctGetterColumn(title=_('User'),
                        getter=getUserName,
                        cell_formatter=fsearch_user_formatter),
        IctGetterColumn(title=_('Room'),
                        getter=lambda i,f: i.room,
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



class AllMiscPhysicals(Overview):
    def objs(self):
        """List of all objects with selected interface"""
        retList = []
        uidutil = queryUtility(IIntIds)
        for (oid, oobj) in uidutil.items():
            if IMiscPhysical.providedBy(oobj.object):
                retList.append(oobj.object)
        return retList


