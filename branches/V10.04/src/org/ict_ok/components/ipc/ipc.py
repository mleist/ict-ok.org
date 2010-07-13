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
"""implementation of IndustrialComputer"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.device.device import Device, DeviceFolder
from org.ict_ok.components.ipc.interfaces \
    import IIndustrialComputer, IIndustrialComputerFolder, IAddIndustrialComputer
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates

def AllIndustrialComputerTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IIndustrialComputer)

def AllIndustrialComputers(dummy_context):
    return AllComponents(dummy_context, IIndustrialComputer)


class IndustrialComputer(Device):
    """
    the template instance
    """
    implements(IIndustrialComputer)
    shortName = "ipc"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    fullTextSearchFields = []
    fullTextSearchFields.extend(Device.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Device.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(IndustrialComputer)
        for (name, value) in data.items():
            if name in IIndustrialComputer.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(IndustrialComputer)

    def store_refs(self, **data):
        Device.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class IndustrialComputerFolder(DeviceFolder):
    implements(IIndustrialComputerFolder,
               IAddIndustrialComputer)
    contentFactory = IndustrialComputer
    shortName = "ipc folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        DeviceFolder.__init__(self, **data)
