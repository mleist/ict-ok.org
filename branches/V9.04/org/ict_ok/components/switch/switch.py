# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 399M 2009-02-02 22:29:31Z (lokal) $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Switch"""

__version__ = "$Id: template.py_cog 399M 2009-02-02 22:29:31Z (lokal) $"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.folder import Folder

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.switch.interfaces import \
    IAddSwitch, ISwitch, ISwitchFolder
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import Component
from org.ict_ok.components.device.device import Device, DeviceFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.rack.rack import Rack_Switches_RelManager
from org.ict_ok.components.patchport.interfaces import IPatchPort
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.physical_component.physical_component import \
    PhysicalComponent

def AllSwitchTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, ISwitch)

def AllSwitches(dummy_context):
    return AllComponents(dummy_context, ISwitch)

def AllUnusedOrUsedRackSwitches(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, ISwitch, 'rack')


#Switch_Interfaces_RelManager = \
#       FieldRelationManager(ISwitch['interfaces'],
#                            IInterface['switch'],
#                            relType='switch:interfaces')




class Switch(Device):
    """
    the template instance
    """
    implements(ISwitch)
    shortName = "switch"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    ifCount = FieldProperty(ISwitch['ifCount'])
    rack = RelationPropertyIn(Rack_Switches_RelManager)
#    patchports = RelationPropertyOut(Switch_PatchPorts_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(Device.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        Device.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Switch)
        print "dddd: ", refAttributeNames
        for (name, value) in data.items():
            if name in ISwitch.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        Device.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(Switch)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class SwitchFolder(DeviceFolder):
    implements(ISwitchFolder,
               IImportCsvData,
               IImportXlsData,
               IAddSwitch)
    def __init__(self, **data):
        """
        constructor of the object
        """
        DeviceFolder.__init__(self, **data)
