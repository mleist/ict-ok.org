# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
#
"""implementation of browser class of Building object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import button
from z3c.form.browser import checkbox
from z3c.blobfile.interfaces import IBlobFile
from z3c.blobfile.file import File as BlobFile

# ict_ok.org imports
from org.ict_ok.libs.document import Document
from org.ict_ok.libs.interfaces import IDocument
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.building.interfaces import IBuilding, IAddBuilding
from org.ict_ok.components.building.building import Building
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm, SuperclassDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddDocument(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Document')
    viewURL = 'add_document.html'
    weight = 90


# --------------- object details ---------------------------


class DocumentDetails(SuperclassDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SuperclassDetails.omit_viewfields + []
    omit_addfields = SuperclassDetails.omit_addfields + []
    omit_editfields = SuperclassDetails.omit_editfields + []


# --------------- forms ------------------------------------


class DetailsBuildingForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of building')
    factory = Building
    omitFields = DocumentDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

    
class AddDocumentForm(AddForm):
    label = _(u'Add Document')
    factory = Document
    attrInterface = IDocument
    omitFields = DocumentDetails.omit_addfields
    fields = fieldsForFactory(factory, omitFields, additionalInterfaces=[IBlobFile])

    def create(self, data):
        """ will create the object """
        obj = AddForm.create(self, data)
        BlobFile.__init__(obj, data['data'], data['contentType'])
        return obj


class EditDocumentForm(EditForm):
    """ Edit for for net """
    label = _(u'Document Form')
    factory = Document
    omitFields = DocumentDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields, additionalInterfaces=[IBlobFile])


class DeleteDocumentForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this document: '%s'?") % \
               IBrwsOverview(self.context).getTitle()

#    @button.buttonAndHandler(u'Delete')
#    def handleDelete(self, action):
#        """delete was pressed"""
#        del self.context._blob
#        DeleteForm.handleDelete(self, action)
