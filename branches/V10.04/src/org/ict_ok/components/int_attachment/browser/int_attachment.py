# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 529 2009-05-14 17:46:43Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of InternalAttachment"""

__version__ = "$Id: template.py_cog 529 2009-05-14 17:46:43Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.app.rotterdam.xmlobject import setNoCacheHeaders
from zope.app import zapi

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox
from z3c.blobfile.file import File

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.int_attachment.interfaces import \
    IInternalAttachment, IAddInternalAttachment, IInternalAttachmentFolder
from org.ict_ok.components.int_attachment.int_attachment import InternalAttachment
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddInternalAttachment(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Internal Attachment')
    viewURL = 'add_int_attachment.html'
    weight = 50


class MGlobalAddInternalAttachment(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Internal Attachment')
    viewURL = 'add_int_attachment.html'
    weight = 50
    folderInterface = IInternalAttachmentFolder

# --------------- object details ---------------------------

from zope.proxy import removeAllProxies

class InternalAttachmentDetails(ComponentDetails):
    """ Class for InternalAttachment details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []

    def download(self):
        upfile = removeAllProxies(self.context.file)
        if self.request is not None:
            self.request.response.setHeader('Content-Type',
                                            self.context.contentType)
            self.request.response.setHeader('Content-Length',
                                            upfile.getSize())
            self.request.response.setHeader(\
                'Content-Disposition',
                u'attachment; filename=\"%s\"' % self.context.filename)
        setNoCacheHeaders(self.request.response)
        return upfile.openDetached()

    def getDownloadHref(self):
        href = zapi.absoluteURL(self.context, self.request)
        title = self.context.ikName
        return u'<a href="%s/@@download.html">-> %s</a>' % (href, title)
        
#        filename = datetime.now().strftime('ictrpt_%Y%m%d%H%M%S.pdf')
#        f_handle, f_name = tempfile.mkstemp(filename)
#        authorStr = self.request.principal.title
#        my_formatter = self.request.locale.dates.getFormatter(
#            'dateTime', 'medium')
#        userTZ = getUserTimezone()
#        longTimeString = my_formatter.format(\
#            userTZ.fromutc(datetime.utcnow()))
#        versionStr = "%s [%s]" % (longTimeString, getIkVersion())
#        self.context.generatePdf(f_name, authorStr, versionStr,request=self.request)
#        self.request.response.setHeader('Content-Type', 'application/pdf')
#        self.request.response.setHeader(\
#            'Content-Disposition',
#            'attachment; filename=\"%s\"' % filename)
#        setNoCacheHeaders(self.request.response)
#        datafile = open(f_name, "r")
#        dataMem = datafile.read()
#        datafile.close()
#        os.remove(f_name)
#        return dataMem


class InternalAttachmentFolderDetails(ComponentDetails):
    """ Class for InternalAttachment details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IInternalAttachment
    factory = InternalAttachment
    omitFields = InternalAttachmentDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsInternalAttachmentForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Internal Attachment')
    factory = InternalAttachment
    omitFields = InternalAttachmentDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

from z3c.form.field import Fields
from z3c.form.browser.file import FileFieldWidget
from zope.traversing.browser import absoluteURL

class AddInternalAttachmentForm(AddComponentForm):
    """Add Internal Attachment form"""
    label = _(u'Add Internal Attachment')
    factory = InternalAttachment
    attrInterface = IInternalAttachment
    addInterface = IAddInternalAttachment
    omitFields = InternalAttachmentDetails.omit_addfields
    allFields = Fields(IInternalAttachment['data'])
    addFields = allFields
    allFields['data'].widgetFactory = FileFieldWidget
    _session_key = 'org.ict_ok.components.int_attachment'

    def create2(self, data):
        """ will create the object """
        obj = self.factory(**data)
        self.newdata = data
        IBrwsOverview(obj).setTitle(data['ikName'])
        obj.__post_init__()
        return obj

    def create(self, data):
        """ will create the object """
        filename = unicode(self.widgets['data'].value.filename)
        data['ikName'] = filename
        data['filename'] = filename
        data['contentType'] = unicode(self.widgets['data'].value.headers['content-type'])
        obj = self.factory(**data)
        self.newdata = data
        IBrwsOverview(obj).setTitle(data['ikName'])
        obj.__post_init__()
        return obj
#        self.filename = self.widgets['data'].value.filename
#        self.contentType = self.widgets['data'].value.headers['content-type']
#        self.widgets['data']
#        obj = File(data['data'], self.contentType)
#        obj.filename = self.widgets['data'].value.filename
#        #zope.event.notify(lifecycleevent.ObjectCreatedEvent(obj))
#        return obj

#    def add(self, obj):
#        """ will store the new one in object tree """
#        travp = self.context
#        # store obj id for nextURL()
#        #self._newObjectID = obj.objectID
#        #while IPagelet.providedBy(travp):
#            #travp = self.context.__parent__
#        travp[obj.filename] = obj
#        if hasattr(obj, "store_refs"):
#            obj.store_refs(**self.newdata)
#        # workaround for gocept.objectquery
#        #import transaction
#        #transaction.savepoint()
#        return obj
#
#    def nextURL(self):
#        """ forward the browser """
#        return absoluteURL(self.context[self.filename],
#                           self.request)



class EditInternalAttachmentForm(EditForm):
    """ Edit for Internal Attachment """
    label = _(u'Internal Attachment Edit Form')
    factory = InternalAttachment
    omitFields = InternalAttachmentDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteInternalAttachmentForm(DeleteForm):
    """ Delete the Internal Attachment """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this InternalAttachment: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = InternalAttachment
    attrInterface = IInternalAttachment
    omitFields = InternalAttachmentDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.int_attachment.int_attachment.InternalAttachment'
    allFields = fieldsForInterface(attrInterface, [])
