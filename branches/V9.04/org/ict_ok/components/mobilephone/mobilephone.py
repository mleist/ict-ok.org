# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of MobilePhone"""

__version__ = "$Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $"

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
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.mobilephone.interfaces import IMobilePhone
from org.ict_ok.components.mobilephone.interfaces import IMobilePhoneFolder, \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.component import Component

def AllMobilePhones(dummy_context):
    """Which MobilePhone are there
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if IMobilePhone.providedBy(oobj.object):
            myString = u"%s" % (oobj.object.getDcTitle())
            terms.append(SimpleTerm(oobj.object,
                                    token=oid,
                                    title=myString))
    return SimpleVocabulary(terms)

def AllXlsCodepages(dummy_context):
    """Which MobilePhone are there
    """
    terms = []
    encodings = {
        0x016F: 'ascii',     #ASCII
        0x01B5: 'cp437',     #IBM PC CP-437 (US)
        0x02D0: 'cp720',     #IBM PC CP-720 (OEM Arabic)
        0x02E1: 'cp737',     #IBM PC CP-737 (Greek)
        0x0307: 'cp775',     #IBM PC CP-775 (Baltic)
        0x0352: 'cp850',     #IBM PC CP-850 (Latin I)
        0x0354: 'cp852',     #IBM PC CP-852 (Latin II (Central European))
        0x0357: 'cp855',     #IBM PC CP-855 (Cyrillic)
        0x0359: 'cp857',     #IBM PC CP-857 (Turkish)
        0x035A: 'cp858',     #IBM PC CP-858 (Multilingual Latin I with Euro)
        0x035C: 'cp860',     #IBM PC CP-860 (Portuguese)
        0x035D: 'cp861',     #IBM PC CP-861 (Icelandic)
        0x035E: 'cp862',     #IBM PC CP-862 (Hebrew)
        0x035F: 'cp863',     #IBM PC CP-863 (Canadian (French))
        0x0360: 'cp864',     #IBM PC CP-864 (Arabic)
        0x0361: 'cp865',     #IBM PC CP-865 (Nordic)
        0x0362: 'cp866',     #IBM PC CP-866 (Cyrillic (Russian))
        0x0365: 'cp869',     #IBM PC CP-869 (Greek (Modern))
        0x036A: 'cp874',     #Windows CP-874 (Thai)
        0x03A4: 'cp932',     #Windows CP-932 (Japanese Shift-JIS)
        0x03A8: 'cp936',     #Windows CP-936 (Chinese Simplified GBK)
        0x03B5: 'cp949',     #Windows CP-949 (Korean (Wansung))
        0x03B6: 'cp950',     #Windows CP-950 (Chinese Traditional BIG5)
        0x04B0: 'utf_16_le', #UTF-16 (BIFF8)
        0x04E2: 'cp1250',    #Windows CP-1250 (Latin II) (Central European)
        0x04E3: 'cp1251',    #Windows CP-1251 (Cyrillic)
        0x04E4: 'cp1252',    #Windows CP-1252 (Latin I) (BIFF4-BIFF7)
        0x04E5: 'cp1253',    #Windows CP-1253 (Greek)
        0x04E6: 'cp1254',    #Windows CP-1254 (Turkish)
        0x04E7: 'cp1255',    #Windows CP-1255 (Hebrew)
        0x04E8: 'cp1256',    #Windows CP-1256 (Arabic)
        0x04E9: 'cp1257',    #Windows CP-1257 (Baltic)
        0x04EA: 'cp1258',    #Windows CP-1258 (Vietnamese)
        0x0551: 'cp1361',    #Windows CP-1361 (Korean (Johab))
        0x2710: 'mac_roman', #Apple Roman
    }
    for codepage in encodings.values():
        terms.append(SimpleTerm(codepage,
                                token=codepage,
                                title=codepage))
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

    fullTextSearchFields = ['phoneNumber', 'contractModel',
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
            if name in IMobilePhone.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        refAttributeNames = getRefAttributeNames(MobilePhone)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class MobilePhoneFolder(Superclass, Folder):
    implements(IMobilePhoneFolder, 
               IImportCsvData,
               IImportXlsData)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
