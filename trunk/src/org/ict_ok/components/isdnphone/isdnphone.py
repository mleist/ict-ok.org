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
"""implementation of ISDNPhone"""

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
from org.ict_ok.components.isdnphone.interfaces import IISDNPhone
from org.ict_ok.components.isdnphone.interfaces import IISDNPhoneFolder
from org.ict_ok.components.isdnphone.interfaces import IAddISDNPhone
from org.ict_ok.components.component import Component
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.osi import osi
from org.ict_ok.components.physical_link.physical_link import \
    PhysicalLinks_PhysicalConnectors_RelManager
from org.ict_ok.components.physical_component.physical_component import \
    PhysicalComponent
from org.ict_ok.components.physical_connector.interfaces import \
    IPhysicalConnector#, IPhysicalConnectorFolder, IAddPhysicalConnector

def AllISDNPhoneTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IISDNPhone)

def AllISDNPhones(dummy_context):
    return AllComponents(dummy_context, IISDNPhone)







class ISDNPhone(PhysicalComponent):
    """
    the template instance
    """
    implements(IISDNPhone)
    shortName = "isdnphone"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    phoneNumber = FieldProperty(IISDNPhone['phoneNumber'])

    connectorPinout = FieldProperty(IPhysicalConnector['connectorPinout'])
    links = RelationPropertyIn(PhysicalLinks_PhysicalConnectors_RelManager)

    fullTextSearchFields = ['phoneNumber']
    fullTextSearchFields.extend(PhysicalComponent.fullTextSearchFields)
        


    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalComponent.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(ISDNPhone)
        for (name, value) in data.items():
            if name in IISDNPhone.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(ISDNPhone)

    def store_refs(self, **data):
        PhysicalComponent.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class ISDNPhoneFolder(Superclass, Folder):
    implements(IISDNPhoneFolder,
               IImportCsvData,
               IImportXlsData,
               IAddISDNPhone)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
