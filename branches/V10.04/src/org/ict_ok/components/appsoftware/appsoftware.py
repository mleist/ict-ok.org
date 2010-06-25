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
"""implementation of ApplicationSoftware"""

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
from org.ict_ok.components.appsoftware.interfaces import \
    IAddApplicationSoftware, IApplicationSoftware, IApplicationSoftwareFolder
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.device.device import Device_AppSoftware_RelManager
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents


def AllApplicationSoftwareTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IApplicationSoftware)

def AllApplicationSoftwares(dummy_context):
    return AllComponents(dummy_context, IApplicationSoftware,
                         True, ['licenseKey'])

def AllUnusedOrUsedDeviceApplicationSoftwares(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IApplicationSoftware,
                                     'device', 'licenseKey')


class ApplicationSoftware(SoftwareComponent):
    """
    the template instance
    """
    implements(IApplicationSoftware)
    shortName = "appsoftware"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    manufacturer = FieldProperty(IApplicationSoftware['manufacturer'])
    otherType = FieldProperty(IApplicationSoftware['otherType'])
    targetOperatingSystems = FieldProperty(IApplicationSoftware['targetOperatingSystems'])
    versionText = FieldProperty(IApplicationSoftware['versionText'])
    licenseKey = FieldProperty(IApplicationSoftware['licenseKey'])
    language = FieldProperty(IApplicationSoftware['language'])
    majorVersion = FieldProperty(IApplicationSoftware['majorVersion'])
    minorVersion = FieldProperty(IApplicationSoftware['minorVersion'])
    revisionNumber = FieldProperty(IApplicationSoftware['revisionNumber'])
    buildNumber = FieldProperty(IApplicationSoftware['buildNumber'])

    device = RelationPropertyIn(Device_AppSoftware_RelManager)

    fullTextSearchFields = ['manufacturer', 'otherType',
                            'targetOperatingSystems', 'versionText',
                            'licenseKey', 'language']
    fullTextSearchFields.extend(SoftwareComponent.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        SoftwareComponent.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(ApplicationSoftware)
        for (name, value) in data.items():
            if name in IApplicationSoftware.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(ApplicationSoftware)

    def store_refs(self, **data):
        SoftwareComponent.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class ApplicationSoftwareFolder(ComponentFolder):
    implements(IApplicationSoftwareFolder,
               IAddApplicationSoftware)
    contentFactory = ApplicationSoftware
    shortName = "appsoftware folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
