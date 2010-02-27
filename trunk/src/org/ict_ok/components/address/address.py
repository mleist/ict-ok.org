# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Address"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# lovely imports
from lovely.relation.property import RelationPropertyIn

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.address.interfaces import IAddress
from org.ict_ok.components.address.interfaces import IAddressFolder
from org.ict_ok.components.address.interfaces import IAddAddress
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.contact_item.contact_item import ContactItem_Addresses_RelManager

def AllAddressTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IAddress)

def AllAddresses(dummy_context):
    return AllComponents(dummy_context, IAddress)

def AllUnusedOrUsedContactItemAddresses(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IAddress, 'contactItem')


class Address(Component):
    """
    the template instance
    """
    implements(IAddress)
    shortName = "address"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    address1 = FieldProperty(IAddress['address1'])
    address2 = FieldProperty(IAddress['address2'])
    address3 = FieldProperty(IAddress['address3'])
    city = FieldProperty(IAddress['city'])
    postalCode = FieldProperty(IAddress['postalCode'])
    country = FieldProperty(IAddress['country'])
    contactItem = RelationPropertyIn(ContactItem_Addresses_RelManager)

    fullTextSearchFields = ['address1', 'address2', 'address3', 'city', 'postalCode', 'country']
    fullTextSearchFields.extend(Component.fullTextSearchFields)
        

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Address)
        for (name, value) in data.items():
            if name in IAddress.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Address)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class AddressFolder(ComponentFolder):
    implements(IAddressFolder,
               IAddAddress)
    contentFactory = Address

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
