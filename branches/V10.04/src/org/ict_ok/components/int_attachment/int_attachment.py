# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of InternalAttachment"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.component import adapter
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports

# z3c imports
from z3c.blobfile.file import File

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.int_attachment.interfaces import IInternalAttachment
from org.ict_ok.components.int_attachment.interfaces import IInternalAttachmentFolder
from org.ict_ok.components.int_attachment.interfaces import IAddInternalAttachment
from zope.app.container.interfaces import IObjectRemovedEvent
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates

def AllInternalAttachmentTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IInternalAttachment)

def AllInternalAttachments(dummy_context):
    return AllComponents(dummy_context, IInternalAttachment)



class InternalAttachment(Component):
    """
    the template instance
    """
    implements(IInternalAttachment)
    shortName = "int_attachment"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    filename = FieldProperty(IInternalAttachment['filename'])
    contentType = FieldProperty(IInternalAttachment['contentType'])
    #data = FieldProperty(IInternalAttachment['data'])

    fullTextSearchFields = []
    fullTextSearchFields.extend(Component.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(InternalAttachment)
        filedata = data.pop('data')
        for (name, value) in data.items():
            if name in IInternalAttachment.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        file = File(filedata, data['contentType'])
        setattr(self, 'file', file)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(InternalAttachment)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


@adapter(IInternalAttachment, IObjectRemovedEvent)
def notifyRemovedEvent(instance, event):
    del instance.file._blob
    del instance.file


class InternalAttachmentFolder(ComponentFolder):
    implements(IInternalAttachmentFolder,
               IAddInternalAttachment)
    contentFactory = InternalAttachment
    shortName = "int_attachment folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
