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
"""implementation of PhysicalConnector"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.folder import Folder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.physical_connector.interfaces import \
    IPhysicalConnector#, IPhysicalConnectorFolder, IAddPhysicalConnector
from org.ict_ok.components.physical_link.interfaces import \
    IPhysicalLink, IPhysicalLinkFolder, IAddPhysicalLink
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import Component
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
#from org.ict_ok.components.room.room import Room_PhysicalConnectors_RelManager

#def AllPhysicalConnectorTemplates(dummy_context):
#    return AllComponentTemplates(dummy_context, IPhysicalConnector)

def PhysicalLinkMediaTypes(dummy_context):
    terms = []
    for (gkey, gname) in {
        0: u"Unknown",
        1: u"Other",
        2: u"Cat1",
        3: u"Cat2",
        4: u"Cat3",
        5: u"Cat4",
        6: u"Cat5",
        7: u"50-ohm Coaxial",
        8: u"75-ohm Coaxial",
        9: u"100-ohm Coaxial",
        10: u"Fiber-optic",
        11: u"UTP",
        12: u"STP",
        13: u"Ribbon Cable",
        14: u"Twinaxial",
        15: u"Optical 9um",
        16: u"Optical 50um",
        17: u"Optical 62.5um",
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)


def AllPhysicalLinkTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IPhysicalLink)

def AllPhysicalLinks(dummy_context):
    return AllComponents(dummy_context, IPhysicalLink)

def AllUnusedOrUsedPhysicalConnectorsPhysicalLinks(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IPhysicalLink, 'connectors')


#
#def AllPhysicalConnectors(dummy_context):
#    return AllComponents(dummy_context, IPhysicalConnector)

#def AllUnusedOrUsedRoomPhysicalConnectors(dummy_context):
#    return AllUnusedOrSelfComponents(dummy_context, IPhysicalConnector, 'room')
#
#def AllUnusedOrUsedInterfacePhysicalConnectors(dummy_context):
#    return AllUnusedOrSelfComponents(dummy_context, IPhysicalConnector, 'interface')

#def AllUnusedOrUsedPhysicalConnectorPhysicalConnectors(dummy_context):
#    return AllUnusedOrSelfComponents(dummy_context, IPhysicalConnector, 'physicalConnector')


#PhysicalConnector_PhysicalConnector_RelManager = \
#    FieldRelationManager(IPhysicalConnector['remote'],
#                         IPhysicalConnector['remote'],
#                         relType='physicalConnector:physicalConnector')
#PhysicalConnector_PhysicalConnector_RelManager = \
#    FieldRelationManager(IPhysicalConnector['local'],
#                         IPhysicalConnector['remote'],
#                         relType='physicalConnector:local:remote')

PhysicalLinks_PhysicalConnectors_RelManager = \
       FieldRelationManager(IPhysicalLink['connectors'],
                            IPhysicalConnector['links'],
                            relType='links:connectors')






class PhysicalLink(Component):
    """
    the template instance
    """
    implements(IPhysicalLink)
    shortName = "physicallink"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    length = FieldProperty(IPhysicalLink['length'])
    maxLength = FieldProperty(IPhysicalLink['maxLength'])
    mediaType = FieldProperty(IPhysicalLink['mediaType'])
    wired = FieldProperty(IPhysicalLink['wired'])
    connectorPinout = FieldProperty(IPhysicalLink['connectorPinout'])

    connectors = RelationPropertyOut(PhysicalLinks_PhysicalConnectors_RelManager)

    fullTextSearchFields = ['connectorPinout']
    fullTextSearchFields.extend(Component.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(PhysicalLink)
        for (name, value) in data.items():
            if name in IPhysicalLink.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(PhysicalLink)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)

    def getAllPhysicalConnectors(self, connectorSet, maxDepth=10):
        if maxDepth < 0:
            raise Exception
        for connector in self.connectors:
            if IPhysicalConnector.providedBy(connector):
                connectorSet.add(connector)
                connector.getAllPhysicalConnectors(connectorSet, maxDepth-1)


class PhysicalLinkFolder(Superclass, Folder):
    implements(IPhysicalLinkFolder,
               IImportCsvData,
               IImportXlsData,
               IAddPhysicalLink)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)


#class PhysicalConnector(Component):
#    """
#    the template instance
#    """
#    implements(IPhysicalConnector)
#    shortName = "physical_connector"
#    # for ..Contained we have to:
#    __name__ = __parent__ = None
#    
#    connectorPinout = FieldProperty(IPhysicalConnector['connectorPinout'])
#    
#    room = RelationPropertyIn(Room_PhysicalConnectors_RelManager)
#
#    interface = RelationPropertyIn(PhysicalConnector_Interface_RelManager)
#
#    fullTextSearchFields = ['connectorPinout']
#    fullTextSearchFields.extend(Component.fullTextSearchFields)
#
#    def __init__(self, **data):
#        """
#        constructor of the object
#        """
#        Component.__init__(self, **data)
#        refAttributeNames = getRefAttributeNames(PhysicalConnector)
#        for (name, value) in data.items():
#            if name in IPhysicalConnector.names():
#                if name not in refAttributeNames:
#                    setattr(self, name, value)
#        self.ikRevision = __version__
#
#    def store_refs(self, **data):
#        refAttributeNames = getRefAttributeNames(PhysicalConnector)
#        for (name, value) in data.items():
#            if name in refAttributeNames:
#                setattr(self, name, value)
#
#
#class PhysicalConnectorFolder(Superclass, Folder):
#    implements(IPhysicalConnectorFolder, 
#               IImportCsvData,
#               IImportXlsData,
#               IAddPhysicalConnector)
#    def __init__(self, **data):
#        """
#        constructor of the object
#        """
#        Superclass.__init__(self, **data)
#        Folder.__init__(self)


#from zope.interface import implements
#from zope.component import adapts
#from org.ict_ok.osi.interfaces import IOSIModel
#
#
#
#class OSIModel(object):
#    """ISized adapter."""
#
#    implements(IOSIModel)
#    adapts(IPhysicalLink)
#
#    def __init__(self, context):
#        self.context = context
#        
#    def connectedComponentsOnLayer1(self, targetSet, searchDepth):
#        """returns a set of components which are connected on layer 1
#
#        targetSet: set of connected components
#        searchDepth: searchDepth will be decreased on every recursive step
#        """
#        print "%s -> connectedComponentsOnLayer1(%s, %s) " % (self.context.ikName, targetSet, searchDepth)
#        if searchDepth < 0:
#            raise Exception
#        if self.context not in targetSet:
#            print "add(%s)" % (self.context.ikName)
#            targetSet.add(self.context)
#            for obj in self.context.connectors:
#                nextOSIModelAdapter = IOSIModel(obj)
#                if nextOSIModelAdapter:
#                    nextOSIModelAdapter.connectedComponentsOnLayer1(targetSet, searchDepth-1)


from zope.component import adapts
from org.ict_ok.osi.interfaces import IPhysicalLayer
from org.ict_ok.osi import osi

class OSIModel(osi.OSIModel):
    """OSI adapter."""

    adapts(IPhysicalLink)
    linkedObjects = {IPhysicalLayer: ['connectors']}
