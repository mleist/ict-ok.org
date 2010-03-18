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
"""implementation of browser class of PatchPort"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implementedBy
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.patchport.interfaces import \
    IPatchPort, IAddPatchPort, IPatchPortFolder
from org.ict_ok.components.patchport.patchport import PatchPort
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm
from org.ict_ok.components.physical_connector.interfaces import \
    IPhysicalConnector#, IPhysicalConnectorFolder, IAddPhysicalConnector

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddPatchPort(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Patch port')
    viewURL = 'add_patchport.html'
    weight = 50


class MGlobalAddPatchPort(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Patch port')
    viewURL = 'add_patchport.html'
    weight = 50
    folderInterface = IPatchPortFolder

# --------------- object details ---------------------------


class PatchPortDetails(ComponentDetails):
    """ Class for PatchPort details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class PatchPortFolderDetails(ComponentDetails):
    """ Class for PatchPort details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IPatchPort
    factory = PatchPort
    omitFields = PatchPortDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsPatchPortForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Patch port')
    factory = PatchPort
    omitFields = PatchPortDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddPatchPortForm(AddComponentForm):
    """Add Patch port form"""
    label = _(u'Add Patch port')
    factory = PatchPort
    attrInterface = IPatchPort
    addInterface = IAddPatchPort
    omitFields = PatchPortDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields, [IPhysicalConnector])
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.patchport'


class EditPatchPortForm(EditForm):
    """ Edit for Patch port """
    label = _(u'Patch port Edit Form')
    factory = PatchPort
    omitFields = PatchPortDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields, [IPhysicalConnector])


class DeletePatchPortForm(DeleteForm):
    """ Delete the Patch port """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this PatchPort: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IPatchPort
    factory = PatchPort
    factoryId = u'org.ict_ok.components.patchport.patchport.PatchPort'
    allFields = fieldsForInterface(attrInterface, [])
