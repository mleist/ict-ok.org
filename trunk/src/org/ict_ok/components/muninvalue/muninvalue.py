# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=F0401,E1101,E0611,W0703,W0612,W0142
#
"""implementation of Latency

Latency does ....

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.folder import Folder

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.latency.interfaces import ILatency
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData


def AllMuninValueTemplates(dummy_context):
    """Which MobilePhone templates exists
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if ILatency.providedBy(oobj.object) and \
        oobj.object.isTemplate:
            myString = u"%s [T]" % (oobj.object.getDcTitle())
            terms.append(SimpleTerm(oobj.object,
                                    token=getattr(oobj.object, 'objectID', oid),
                                    title=myString))
    return SimpleVocabulary(terms)


class Latency(Component):
    """
    the template instance
    """

    implements(ILatency)
    shortName = "value"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    checkcount = FieldProperty(ILatency['checkcount'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        for (name, value) in data.items():
            if name in ILatency.names():
                setattr(self, name, value)
        self.ikRevision = __version__
        
    def get_health(self):
        return None

    def tickerEvent(self):
        """ trigger from ticker
        """
        pass
        
    def triggerMin(self):
        """ got ticker event from ticker thread every minute
        """
        print "Unsinn"


class MuninValueFolder(Superclass, Folder):
    implements(IMobilePhoneFolder, 
               IImportCsvData,
               IImportXlsData,
               IAddMobilePhones)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
