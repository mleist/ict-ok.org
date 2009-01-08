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
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

from lovely.relation.property import RelationPropertyIn

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.host.host import Host_Interfaces_RelManager
   

def AllInterfaces(dummy_context):
    """In which production state a host may be
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if IInterface.providedBy(oobj.object):
            myString = u"%s" % (oobj.object.getDcTitle())
            terms.append(\
                SimpleTerm(oobj.object,
                           token=oid,
                           title=myString))
    return SimpleVocabulary(terms)
        
#def documentsInParentVocabulary(context):

    #"""a vocabulary that returns the child documents __name__for any
    #subobjects of parent"""

    #return SimpleVocabulary.fromItems(
        #[(k, v) for k, v in context.__parent__.items() \
         #if IDocument.providedBy(v)])



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
    
    host2 = RelationPropertyIn(Host_Interfaces_RelManager)
    
    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        for (name, value) in data.items():
            if name in IInterface.names():
                setattr(self, name, value)
        self.ikRevision = __version__
