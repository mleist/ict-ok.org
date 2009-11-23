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
"""implementation of PersonalComputer"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.folder import Folder

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.device.device import Device, DeviceFolder
from org.ict_ok.components.pc.interfaces import \
    IPersonalComputer, IPersonalComputerFolder, IAddPersonalComputer
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents

def AllPersonalComputerTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IPersonalComputer)

def AllPersonalComputers(dummy_context):
    return AllComponents(dummy_context, IPersonalComputer)







class PersonalComputer(Device):
    """
    the template instance
    """
    implements(IPersonalComputer)
    shortName = "pc"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    fullTextSearchFields = []
    fullTextSearchFields.extend(Device.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Device.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(PersonalComputer)
        for (name, value) in data.items():
            if name in IPersonalComputer.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(PersonalComputer)

    def store_refs(self, **data):
        Device.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class PersonalComputerFolder(DeviceFolder):
    implements(IPersonalComputerFolder,
               IAddPersonalComputer)
    def __init__(self, **data):
        """
        constructor of the object
        """
        DeviceFolder.__init__(self, **data)
