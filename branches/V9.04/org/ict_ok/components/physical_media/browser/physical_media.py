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
"""implementation of browser class of PhysicalMedia"""

__version__ = "$Id$"

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
from org.ict_ok.components.physical_media.interfaces import \
    IPhysicalMedia, IAddPhysicalMedia, IPhysicalMediaFolder
from org.ict_ok.components.physical_media.physical_media import PhysicalMedia
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
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
from org.ict_ok.libs.physicalquantity import convertQuantity, physq
_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddPhysicalMedia(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Physical Media')
    viewURL = 'add_physical_media.html'
    weight = 50


class MGlobalAddPhysicalMedia(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Physical Media')
    viewURL = 'add_physical_media.html'
    weight = 50
    folderInterface = IPhysicalMediaFolder


class MSubInvPhysicalMedia(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All Physical Media')
    viewURL = '/@@all_physical_medias.html'
    weight = 100

# --------------- object details ---------------------------


class PhysicalMediaDetails(PhysicalComponentDetails):
    """ Class for PhysicalMedia details
    """
    omit_viewfields = PhysicalComponentDetails.omit_viewfields + []
    omit_addfields = PhysicalComponentDetails.omit_addfields + []
    omit_editfields = PhysicalComponentDetails.omit_editfields + []
    
    def convertQuantity(self, quantityString):
        return convertQuantity(quantityString)

    def adjustQuantity(self, quantity):
        return quantity.ounit('Gb')

class PhysicalMediaFolderDetails(ComponentDetails):
    """ Class for PhysicalMedia details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IPhysicalMedia
    factory = PhysicalMedia
    omitFields = PhysicalMediaDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsPhysicalMediaForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Physical Media')
    factory = PhysicalMedia
    omitFields = PhysicalMediaDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddPhysicalMediaForm(AddComponentForm):
    """Add Physical Media form"""
    label = _(u'Add Physical Media')
    factory = PhysicalMedia
    attrInterface = IPhysicalMedia
    addInterface = IAddPhysicalMedia
    omitFields = PhysicalMediaDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.physical_media'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditPhysicalMediaForm(EditForm):
    """ Edit for Physical Media """
    label = _(u'Physical Media Edit Form')
    factory = PhysicalMedia
    omitFields = PhysicalMediaDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeletePhysicalMediaForm(DeleteForm):
    """ Delete the Physical Media """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this PhysicalMedia: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = PhysicalMedia
    attrInterface = IPhysicalMedia
    omitFields = PhysicalMediaDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.physical_media.physical_media.PhysicalMedia'
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



class AllPhysicalMedia(Overview):
    def objs(self):
        """List of all objects with selected interface"""
        retList = []
        uidutil = queryUtility(IIntIds)
        for (oid, oobj) in uidutil.items():
            if IPhysicalMedia.providedBy(oobj.object):
                retList.append(oobj.object)
        return retList


