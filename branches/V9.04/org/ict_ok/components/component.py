# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""superclass for all content-objects
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.components.supernode.supernode import Supernode


def AllComponentTemplates(dummy_context, interface):
    """Which MobilePhone templates exists
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if interface.providedBy(oobj.object) and \
        oobj.object.isTemplate:
            myString = u"%s [T]" % (oobj.object.getDcTitle())
            terms.append(SimpleTerm(oobj.object,
                                    token=oid,
                                    title=myString))
    terms.sort(lambda l, r: cmp(l.title.lower(), r.title.lower()))
    return SimpleVocabulary(terms)

def AllComponents(dummy_context, interface, additionalAttrNames=None):
    """In which production state a host may be
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if interface.providedBy(oobj.object):
            myString = u"%s" % (oobj.object.getDcTitle())
            if additionalAttrNames is not None:
                for additionalAttrName in additionalAttrNames:
                    additionalAttribute = getattr(oobj.object, additionalAttrName)
                    if additionalAttribute is not None:
                        if hasattr(additionalAttribute, 'ikName'):
                            if len(additionalAttribute.ikName) > 10:
                                dotted = u'...)'
                            else:
                                dotted = u')'
                            myString = myString + u" (%s" % \
                                additionalAttribute.ikName[:10] + dotted
                        else:
                            if len(additionalAttribute) > 10:
                                dotted = u'...)'
                            else:
                                dotted = u')'
                            myString = myString + u" (%s" % \
                                additionalAttribute[:10] + dotted
            terms.append(\
                SimpleTerm(oobj.object,
                           token=oid,
                           title=myString))
    terms.sort(lambda l, r: cmp(l.title.lower(), r.title.lower()))
    return SimpleVocabulary(terms)
    
def AllUnusedOrSelfComponents(dummy_context, interface,
                              obj_attr_name, additionalAttrNames=None):
    """In which production state a host may be
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if interface.providedBy(oobj.object):
            if not oobj.object.isTemplate:
                if getattr(oobj.object, obj_attr_name) is None:
                    myString = u"%s" % (oobj.object.getDcTitle())
                    if additionalAttrNames is not None:
                        for additionalAttrName in additionalAttrNames:
                            additionalAttribute = getattr(oobj.object, additionalAttrName)
                            if additionalAttribute is not None:
                                if hasattr(additionalAttribute, 'ikName'):
                                    if len(additionalAttribute.ikName) > 10:
                                        dotted = u'...)'
                                    else:
                                        dotted = u')'
                                    myString = myString + u" (%s" % \
                                        additionalAttribute.ikName[:10] + dotted
                                else:
                                    if len(additionalAttribute) > 10:
                                        dotted = u'...)'
                                    else:
                                        dotted = u')'
                                    myString = myString + u" (%s" % \
                                        additionalAttribute[:10] + dotted
                    terms.append(\
                        SimpleTerm(oobj.object,
                                   token=oid,
                                   title=myString))
                else:
                    if getattr(oobj.object, obj_attr_name) == dummy_context:
                        myString = u"%s" % (oobj.object.getDcTitle())
                        if additionalAttrNames is not None:
                            for additionalAttrName in additionalAttrNames:
                                additionalAttribute = getattr(oobj.object, additionalAttrName)
                                if additionalAttribute is not None:
                                    if hasattr(additionalAttribute, 'ikName'):
                                        if len(additionalAttribute.ikName) > 10:
                                            dotted = u'...)'
                                        else:
                                            dotted = u')'
                                        myString = myString + u" (%s" % \
                                            additionalAttribute.ikName[:10] + dotted
                                    else:
                                        if len(additionalAttribute) > 10:
                                            dotted = u'...)'
                                        else:
                                            dotted = u')'
                                        myString = myString + u" (%s" % \
                                            additionalAttribute[:10] + dotted
                        terms.append(\
                            SimpleTerm(oobj.object,
                                       token=oid,
                                       title=myString))
    terms.sort(lambda l, r: cmp(l.title.lower(), r.title.lower()))
    return SimpleVocabulary(terms)


class Component(Supernode):
    """
    the general component instance
    """

    implements(IComponent)
    isTemplate = FieldProperty(IComponent['isTemplate'])
    requirement = FieldProperty(IComponent['requirement'])

    fullTextSearchFields = []
    fullTextSearchFields.extend(Supernode.fullTextSearchFields)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Supernode.__init__(self, **data)
        #self.myFactory = str(self.__class__).split("'")[1]
        for (name, value) in data.items():
            if name in IComponent.names():
                setattr(self, name, value)
        if not hasattr(self, 'isTemplate'):
            self.isTemplate = False
        self.ikRevision = __version__

    def get_health(self):
        """
        output of health, 0-1 (float)
        !!!!!! has to be implemented by subclass !!!!!!
        """
        #raise Exception, 'Not implemented yet'
        return None
    
    def get_wcnt(self):
        """
        weighted count of accesses
        !!!!!! has to be implemented by subclass !!!!!!
        """
        #raise Exception, 'Not implemented yet'
        return None

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
