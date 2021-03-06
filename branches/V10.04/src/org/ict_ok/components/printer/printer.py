# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Printer"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.printer.interfaces import IPrinter
from org.ict_ok.components.printer.interfaces import IPrinterFolder
from org.ict_ok.components.printer.interfaces import IAddPrinter
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates
from org.ict_ok.components.device.device import Device

def AllPrinterTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IPrinter)

def AllPrinters(dummy_context):
    return AllComponents(dummy_context, IPrinter)


class Printer(Device):
    """
    the template instance
    """
    implements(IPrinter)
    shortName = "printer"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    paperTypesAvailable = FieldProperty(IPrinter['paperTypesAvailable'])

    fullTextSearchFields = ['paperTypesAvailable']
    fullTextSearchFields.extend(Device.fullTextSearchFields)
        

    def __init__(self, **data):
        """
        constructor of the object
        """
        Device.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Printer)
        for (name, value) in data.items():
            if name in IPrinter.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Printer)

    def store_refs(self, **data):
        Device.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class PrinterFolder(ComponentFolder):
    implements(IPrinterFolder,
               IAddPrinter)
    contentFactory = Printer
    shortName = "printer folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
