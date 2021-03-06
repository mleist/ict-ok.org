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
"""implementation of OperatingSoftware"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports
from lovely.relation.property import RelationPropertyIn

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.software_component.software_component import \
    SoftwareComponent
from org.ict_ok.components.osoftware.interfaces import \
    IAddOperatingSoftware, IOperatingSoftware, IOperatingSoftwareFolder
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.device.device import Device_OSoftware_RelManager
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents


def AllOperatingSoftwareTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IOperatingSoftware)

def AllOperatingSoftwares(dummy_context):
    return AllComponents(dummy_context, IOperatingSoftware,
                         True, 'licenseKey')

def AllUnusedOrUsedDeviceOperatingSoftwares(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IOperatingSoftware,
                                     'device', 'licenseKey')


class OperatingSoftware(SoftwareComponent):
    """
    the template instance
    """
    implements(IOperatingSoftware)
    shortName = "osoftware"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    
    manufacturer = FieldProperty(IOperatingSoftware['manufacturer'])
    osType = FieldProperty(IOperatingSoftware['osType'])
    otherType = FieldProperty(IOperatingSoftware['otherType'])
    versionText = FieldProperty(IOperatingSoftware['versionText'])
    licenseKey = FieldProperty(IOperatingSoftware['licenseKey'])
    language = FieldProperty(IOperatingSoftware['language'])
    majorVersion = FieldProperty(IOperatingSoftware['majorVersion'])
    minorVersion = FieldProperty(IOperatingSoftware['minorVersion'])
    revisionNumber = FieldProperty(IOperatingSoftware['revisionNumber'])
    buildNumber = FieldProperty(IOperatingSoftware['buildNumber'])

    device = RelationPropertyIn(Device_OSoftware_RelManager)
    
    fullTextSearchFields = ['manufacturer', 'osType',
                            'otherType', 'versionText',
                            'licenseKey', 'language']
    fullTextSearchFields.extend(SoftwareComponent.fullTextSearchFields)    

    def __init__(self, **data):
        """
        constructor of the object
        """
        SoftwareComponent.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(OperatingSoftware)
        for (name, value) in data.items():
            if name in IOperatingSoftware.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(OperatingSoftware)

    def store_refs(self, **data):
        SoftwareComponent.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class OperatingSoftwareFolder(ComponentFolder):
    implements(IOperatingSoftwareFolder,
               IAddOperatingSoftware)
    contentFactory = OperatingSoftware
    shortName = "osoftware folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
