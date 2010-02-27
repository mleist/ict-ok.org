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
"""implementation of PatchPort"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.interface import Invalid
from zope.schema.fieldproperty import FieldProperty

# lovely imports
from lovely.relation.property import RelationPropertyIn

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.patchport.interfaces import \
    IPatchPort, IPatchPortFolder, IAddPatchPort
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.patchpanel.patchpanel import PatchPanel_PatchPorts_RelManager
from org.ict_ok.components.physical_connector.interfaces import \
    IPhysicalConnector#, IPhysicalConnectorFolder, IAddPhysicalConnector
from org.ict_ok.components.physical_link.physical_link import \
    PhysicalLinks_PhysicalConnectors_RelManager
from org.ict_ok.components.physical_component.physical_component import \
    PhysicalComponent

def AllPatchPortTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IPatchPort)

def AllPatchPorts(dummy_context):
    return AllComponents(dummy_context, IPatchPort)

def AllUnusedOrUsedPatchPanelPatchPorts(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IPatchPort, 'patchpanel')


#FrontLink_PatchPort_RelManager = \
#       FieldRelationManager(IPhysicalLink['connectors'],
#                            IPatchPort['frontLink'],
#                            relType='frontLink:connectors')
#
#RearLink_PatchPort_RelManager = \
#       FieldRelationManager(IPhysicalLink['connectors'],
#                            IPatchPort['rearLink'],
#                            relType='rearLink:connectors')


class PatchPort(PhysicalComponent):
    """
    the template instance
    """
    #implements(IPatchPort, IPhysicalConnector)
    implements(IPatchPort)
    shortName = "patchport"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    #ddd = FieldProperty(IPatchPort['ddd'])

    patchpanel = RelationPropertyIn(PatchPanel_PatchPorts_RelManager)

    connectorPinout = FieldProperty(IPhysicalConnector['connectorPinout'])
    #local = RelationPropertyOut(PhysicalConnector_PhysicalConnector_RelManager)
    #remote = RelationPropertyOut(PhysicalConnector_PhysicalConnector_RelManager)
    links = RelationPropertyIn(PhysicalLinks_PhysicalConnectors_RelManager)
#    frontLink = RelationPropertyIn(FrontLink_PatchPort_RelManager)
#    rearLink = RelationPropertyIn(RearLink_PatchPort_RelManager)
    #, relType='physicalConnector:physicalConnector')

    fullTextSearchFields = []
    fullTextSearchFields.extend(PhysicalComponent.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalComponent.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(PatchPort)
        for (name, value) in data.items():
            if name in IPatchPort.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(PatchPort)

    def store_refs(self, **data):
        PhysicalComponent.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)

    def ensureInvariants(self, formObj):
        if hasattr(formObj, 'room'):
            if self.patchpanel is not None and \
               self.patchpanel.room  is not None and \
               self.patchpanel.room != formObj.room:
                raise Invalid(
                    "Port (%s) and Panel (%s) in different rooms." % \
                    (formObj.room.ikName, self.patchpanel.room.ikName))
               


class PatchPortFolder(ComponentFolder):
    implements(IPatchPortFolder,
               IAddPatchPort)
    contentFactory = PatchPort

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
