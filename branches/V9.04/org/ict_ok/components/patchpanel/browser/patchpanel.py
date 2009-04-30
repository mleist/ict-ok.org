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
"""implementation of browser class of PatchPanel"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox
from zope.lifecycleevent import ObjectCreatedEvent
from zope.event import notify
from zope.component import queryUtility
from zope.app.intid.interfaces import IIntIds

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.patchpanel.interfaces import IPatchPanel, IAddPatchPanel
from org.ict_ok.components.patchpanel.patchpanel import PatchPanel
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm
from org.ict_ok.components.patchport.patchport import PatchPort
from org.ict_ok.components.patchport.interfaces import IPatchPortFolder

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddPatchPanel(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Patch panel')
    viewURL = 'add_patchpanel.html'

    weight = 50

# --------------- object details ---------------------------


class PatchPanelDetails(ComponentDetails):
    """ Class for PatchPanel details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class PatchPanelFolderDetails(ComponentDetails):
    """ Class for PatchPanel details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IPatchPanel
    factory = PatchPanel
    fields = fieldsForFactory(factory, omit_editfields)

# --------------- forms ------------------------------------


class DetailsPatchPanelForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Patch panel')
    factory = PatchPanel
    omitFields = PatchPanelDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddPatchPanelForm(AddComponentForm):
    """Add Patch panel form"""
    label = _(u'Add Patch panel')
    factory = PatchPanel
    omitFields = PatchPanelDetails.omit_addfields
    attrInterface = IPatchPanel
    addInterface = IAddPatchPanel
    _session_key = 'org.ict_ok.components.patchpanel'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = checkbox.SingleCheckBoxFieldWidget

    def createAndAdd(self, data):
        obj = self.create(data)
        notify(ObjectCreatedEvent(obj))
        self.add(obj)
        uidutil = queryUtility(IIntIds)
        oneParent = None
        for (oid, oobj) in uidutil.items():
            if IPatchPortFolder.providedBy(oobj.object):
                oneParent = oobj.object
                break
        if oneParent is not None:
            for i in range(1, obj.portCount+1):
                dataVect = {}
                dataVect['ikName'] = u'%s-%02d' % (obj.ikName, i)
                dataVect['patchpanel'] = obj
                if obj.room is not None:
                    dataVect['room'] = obj.room
                newObj = PatchPort(**dataVect)
                newObj.__post_init__()
                IBrwsOverview(newObj).setTitle(dataVect['ikName'])
                oneParent[newObj.objectID] = newObj
                if hasattr(newObj, "store_refs"):
                    newObj.store_refs(**dataVect)
                notify(ObjectCreatedEvent(newObj))
        return obj



class EditPatchPanelForm(EditForm):
    """ Edit for Patch panel """
    label = _(u'Patch panel Edit Form')
    factory = PatchPanel
    omitFields = PatchPanelDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeletePatchPanelForm(DeleteForm):
    """ Delete the Patch panel """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this PatchPanel: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IPatchPanel
    factory = PatchPanel
    factoryId = u'org.ict_ok.components.patchpanel.patchpanel.PatchPanel'
    allFields = fieldsForInterface(attrInterface, [])
