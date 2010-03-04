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
"""implementation of MiscPhysical"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements

# lovely imports

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.misc_physical.interfaces import IMiscPhysical
from org.ict_ok.components.misc_physical.interfaces import IMiscPhysicalFolder
from org.ict_ok.components.misc_physical.interfaces import IAddMiscPhysical
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates
from org.ict_ok.components.device.device import Device

def AllMiscPhysicalTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IMiscPhysical)

def AllMiscPhysicals(dummy_context):
    return AllComponents(dummy_context, IMiscPhysical)


class MiscPhysical(Device):
    """
    the template instance
    """
    implements(IMiscPhysical)
    shortName = "misc_physical"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    fullTextSearchFields = []
    fullTextSearchFields.extend(Device.fullTextSearchFields)
        

    def __init__(self, **data):
        """
        constructor of the object
        """
        Device.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(MiscPhysical)
        for (name, value) in data.items():
            if name in IMiscPhysical.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(MiscPhysical)

    def store_refs(self, **data):
        Device.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class MiscPhysicalFolder(ComponentFolder):
    implements(IMiscPhysicalFolder,
               IAddMiscPhysical)
    contentFactory = MiscPhysical
    shortName = "misc_physical folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
