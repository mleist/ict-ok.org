# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Interface

Interface does ....

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.folder import Folder

from lovely.relation.property import RelationPropertyIn

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.component import Component
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.interface.interfaces import \
    IInterface, IAddInterface, IInterfaceFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.host.host import Host_Interfaces_RelManager
from org.ict_ok.components.device.device import Device_Interface_RelManager



def AllInterfaceTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IInterface)

def AllInterfaces(dummy_context):
    return AllComponents(dummy_context, IInterface)

def AllUnusedOrUsedDeviceInterfaces(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IInterface, 'device')


class Interface(Component):
    """
    the template instance
    """

    implements(IInterface)
    shortName = "interface"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    netType = FieldProperty(IInterface['netType'])
    mac = FieldProperty(IInterface['mac'])
    ipv4List = FieldProperty(IInterface['ipv4List'])
    
    device = RelationPropertyIn(Device_Interface_RelManager)
    host2 = RelationPropertyIn(Host_Interfaces_RelManager)

    fullTextSearchFields = ['netType', 'mac',
                            'ipv4List']
    fullTextSearchFields.extend(Component.fullTextSearchFields)
    
    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Interface)
        for (name, value) in data.items():
            if name in IInterface.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__
        
    def store_refs(self, **data):
        refAttributeNames = getRefAttributeNames(Interface)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)



class InterfaceFolder(Superclass, Folder):
    implements(IInterfaceFolder, 
               IImportCsvData,
               IImportXlsData,
               IAddInterface)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
