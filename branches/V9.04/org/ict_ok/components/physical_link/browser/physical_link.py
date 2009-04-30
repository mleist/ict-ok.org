# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0613,W0232,W0142
#
"""implementation of browser class of PhysicalConnector"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.traversing.browser import absoluteURL
from zope.app.intid.interfaces import IIntIds
from zope.component import queryUtility
from zope.lifecycleevent import ObjectCreatedEvent, ObjectModifiedEvent
from zope.event import notify

# z3c imports
from z3c.form import button, field, form, interfaces
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.physical_link.interfaces import \
    IPhysicalLink, IAddPhysicalLink, ICreatePhysicalLinks
from org.ict_ok.components.physical_link.physical_link import PhysicalLink
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


class MSubAddPhysicalLink(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add physical link')
    viewURL = 'add_physical_link.html'
    weight = 50


class MSubCreateLinks(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Create physical links wizard')
    viewURL = 'wz_create.html'
    weight = 50


# --------------- object details ---------------------------


class PhysicalLinkDetails(ComponentDetails):
    """ Class for PhysicalConnector details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class PhysicalLinkFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    attrInterface = IPhysicalLink
    factory = PhysicalLink
    fields = fieldsForFactory(factory, omit_editfields)

# --------------- forms ------------------------------------


class DetailsPhysicalLinkForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of physical link')
    factory = PhysicalLink
    omitFields = PhysicalLinkDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddPhysicalLinkForm(AddComponentForm):
    """Add physical link form"""
    label = _(u'Add physical link')
    factory = PhysicalLink
    omitFields = PhysicalLinkDetails.omit_addfields
    attrInterface = IPhysicalLink
    addInterface = IAddPhysicalLink
    _session_key = 'org.ict_ok.components.physical_link'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = checkbox.SingleCheckBoxFieldWidget


class EditPhysicalLinkForm(EditForm):
    """ Edit for physical link """
    label = _(u'physical link Edit')
    factory = PhysicalLink
    omitFields = PhysicalLinkDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeletePhysicalLinkForm(DeleteForm):
    """ Delete the physical link """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this physical link: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class CreatePhysicalLinksForm(EditForm):
    """Create 1-1 physical links between some connectors"""
    label = _(u'Create all lying in between physical links')
    fields = fieldsForInterface(ICreatePhysicalLinks, [])

    def update(self):
        EditForm.update(self)
        self.widgets['connectors'].size = 30
    
    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """cancel was pressed"""
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    @button.buttonAndHandler(_('Create'), name='create')
    def handleCreate(self, action):
        """create was pressed"""
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        objList = data['connectors']
        if len(objList) < 2:
            self.status = _('insufficient connectors')
            return
        else:
            uidutil = queryUtility(IIntIds)
            con1 = objList.pop(0)
            con1_id = uidutil.getId(con1)
            while len(objList) > 0:
                con2 = objList.pop(0)
                con2_id = uidutil.getId(con2)
                print "conn: %s - %s" % (con1.ikName, con2.ikName)
                dataVect = {}
                dataVect['ikName'] = u'%s -/- %s' % (con1.ikName, con2.ikName)
                dataVect['connectors'] = [con1, con2]
                dataVect['requirements'] = []
                newObj = PhysicalLink(**dataVect)
                newObj.__post_init__()
                IBrwsOverview(newObj).setTitle(dataVect['ikName'])
                self.context[newObj.objectID] = newObj
                if hasattr(newObj, "store_refs"):
                    newObj.store_refs(**dataVect)
                notify(ObjectCreatedEvent(newObj))
                con1 = con2
                con1_id = con2_id
            url = absoluteURL(self.context, self.request) + u'/wz_create.html'
            self.request.response.redirect(url)
    


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IPhysicalLink
    factory = PhysicalLink
    factoryId = u'org.ict_ok.components.physical_link.physical_link.PhysicalLink'
    allFields = fieldsForInterface(attrInterface, [])
