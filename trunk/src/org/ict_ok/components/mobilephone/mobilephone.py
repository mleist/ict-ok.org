# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""implementation of MobilePhone"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.folder import Folder

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.mobilephone.interfaces import \
    IMobilePhone, IMobilePhoneFolder, IAddMobilePhone
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import Component

def AllMobilePhones(dummy_context):
    """Which MobilePhone exists
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if IMobilePhone.providedBy(oobj.object):
            myString = u"%s" % (oobj.object.getDcTitle())
            terms.append(SimpleTerm(oobj.object,
                                    token=getattr(oobj.object, 'objectID', oid),
                                    title=myString))
    return SimpleVocabulary(terms)

def AllMobilePhoneTemplates(dummy_context):
    """Which MobilePhone templates exists
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if IMobilePhone.providedBy(oobj.object) and \
        oobj.object.isTemplate:
            myString = u"%s [T]" % (oobj.object.getDcTitle())
            terms.append(SimpleTerm(oobj.object,
                                    token=getattr(oobj.object, 'objectID', oid),
                                    title=myString))
    return SimpleVocabulary(terms)


#MobilePhone_Conns_RelManager = FieldRelationManager(IMobilePhone['conns'],
                                                 #IMobilePhone['conn'],
                                                 #relType='mobilephone:conns')

class MobilePhone(Component):
    """
    the template instance
    """
    implements(IMobilePhone)
    shortName = "mobilephone"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    #attrFoo = FieldProperty(IMobilePhone['attrFoo'])
    #user = FieldProperty(IMobilePhone['user'])
    #pin = FieldProperty(IMobilePhone['pin'])
    #puk = FieldProperty(IMobilePhone['puk'])
    
    phoneNumber = FieldProperty(IMobilePhone['phoneNumber'])
    user = FieldProperty(IMobilePhone['user'])
    contractModel = FieldProperty(IMobilePhone['contractModel'])
    contractEnd = FieldProperty(IMobilePhone['contractEnd'])
    deliveryDate = FieldProperty(IMobilePhone['deliveryDate'])
    modelType = FieldProperty(IMobilePhone['modelType'])
    serialNumber = FieldProperty(IMobilePhone['serialNumber'])
    imei = FieldProperty(IMobilePhone['imei'])
    pin = FieldProperty(IMobilePhone['pin'])
    puk = FieldProperty(IMobilePhone['puk'])
    simNumber = FieldProperty(IMobilePhone['simNumber'])

    fullTextSearchFields = ['phoneNumber', 'user', 'contractModel',
                            'modelType', 'serialNumber',
                            'imei', 'pin', 'puk', 'simNumber']
    fullTextSearchFields.extend(Component.fullTextSearchFields)
    
    #conns = RelationPropertyOut(MobilePhone_Conns_RelManager)
    #conn = RelationPropertyIn(MobilePhone_Conns_RelManager)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(MobilePhone)
        for (name, value) in data.items():
            if name in IMobilePhone.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(MobilePhone)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class MobilePhoneFolder(Superclass, Folder):
    implements(IMobilePhoneFolder, 
               IImportCsvData,
               IImportXlsData,
               IAddMobilePhone)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
