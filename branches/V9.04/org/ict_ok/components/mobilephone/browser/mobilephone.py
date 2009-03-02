# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $
#
# pylint: disable-msg=E1101,W0612,W0232,W0142
#
"""implementation of browser class of MobilePhone"""

__version__ = "$Id: template.py_cog 396 2009-01-08 00:21:51Z markusleist $"

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.mobilephone.interfaces import \
    IMobilePhone, IAddMobilePhone
from org.ict_ok.components.mobilephone.mobilephone import MobilePhone
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

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddMobilePhone(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Mobile phone')
    viewURL = 'add_mobilephone.html'

    weight = 50

# --------------- object details ---------------------------


class MobilePhoneDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']


class MobilePhoneFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    fields = field.Fields(IMobilePhone).omit(*MobilePhoneDetails.omit_viewfields)
    attrInterface = IMobilePhone


# --------------- forms ------------------------------------


# TODO: delete this form
class DetailsMobilePhoneForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Mobile phone')
    factory = MobilePhone
    omitFields = MobilePhoneDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddMobilePhoneForm(AddComponentForm):
    label = _(u"Add Mobile Phones")
    factory = MobilePhone
    attrInterface = IMobilePhone
    addInterface = IAddMobilePhone
    omitFields = MobilePhoneDetails.omit_addfields
    _session_key = 'org.ict_ok.components.mobilephone'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget
        

class EditMobilePhoneForm(EditForm):
    """ Edit for Mobile phone """
    label = _(u'Mobile phone Edit Form')
    factory = MobilePhone
    omitFields = MobilePhoneDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
    fields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class DeleteMobilePhoneForm(DeleteForm):
    """ Delete the Mobile phone """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this MobilePhone: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
#    allFields['isTemplate'].widgetFactory = \
#        checkbox.SingleCheckBoxFieldWidget
    attrInterface = IMobilePhone
    factory = MobilePhone
    factoryId = u'org.ict_ok.components.mobilephone.mobilephone.MobilePhone'
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
