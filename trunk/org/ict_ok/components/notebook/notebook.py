# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Notebook"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.notebook.interfaces import \
    INotebook, INotebookFolder, IAddNotebook
from org.ict_ok.components.device.device import Device, DeviceFolder
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents


def AllNotebookTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, INotebook)

def AllNotebooks(dummy_context):
    return AllComponents(dummy_context, INotebook)

def AllUnusedOrSelfNotebooks(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, INotebook, 'device')


class Notebook(Device):
    """
    the template instance
    """
    implements(INotebook)
    shortName = "notebook"
    
    fullTextSearchFields = []
    fullTextSearchFields.extend(Device.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Device.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Notebook)
        for (name, value) in data.items():
            if name in INotebook.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        Device.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(Notebook)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class NotebookFolder(DeviceFolder):
    implements(INotebookFolder,
               IImportCsvData,
               IImportXlsData,
               IAddNotebook)
    def __init__(self, **data):
        """
        constructor of the object
        """
        DeviceFolder.__init__(self, **data)
