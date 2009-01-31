# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Outlet"""

__version__ = "$Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.outlet.interfaces import \
    IOutlet, IOutletFolder, IAddOutlet
from org.ict_ok.components.physical_connector.physical_connector import \
    PhysicalConnector, PhysicalConnectorFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates


def AllOutletTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IOutlet)

def AllOutlets(dummy_context):
    return AllComponents(dummy_context, IOutlet)


class Outlet(PhysicalConnector):
    """
    the template instance
    """
    implements(IOutlet)
    shortName = "outlet"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    
    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalConnector.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Outlet)
        for (name, value) in data.items():
            if name in IOutlet.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        PhysicalConnector.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(Outlet)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class OutletFolder(PhysicalConnectorFolder):
    implements(IOutletFolder, 
               IAddOutlet)
    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalConnectorFolder.__init__(self, **data)
