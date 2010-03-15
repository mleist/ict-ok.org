# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0702,W0221
#
"""implementation of a "Object-Message-Queue-Utility" 
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component.interfaces import ComponentLookupError
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# ict_ok.org imports
from org.ict_ok.admin_utils.categories.interfaces import \
     IAdmUtilCategories, IAdmUtilCatHostGroup
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar, IAdmUtilEvent
from org.ict_ok.components.superclass.superclass import objectsWithInterface

def AllHostGroups(dummy_context):
    """Which host group are there
    """
    terms = []
    try:
        utilCategories = getUtility(IAdmUtilCategories)
        hostGroups = utilCategories.getHostGroups()
        for hostGroup in hostGroups:
            terms.append(SimpleTerm(hostGroup.objectID,
                                    str(hostGroup.objectID),
                                    hostGroup.ikName))
        return SimpleVocabulary(terms)
    except ComponentLookupError, err:
        return SimpleVocabulary([])


class AdmUtilCatHostGroup(Supernode):
    """Implementation of host group entry."""

    implements(IAdmUtilCatHostGroup)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Supernode.__init__(self, **data)
        for (name, value) in data.items():
            if name in IAdmUtilCatHostGroup.names():
                setattr(self, name, value)
        self.ikRevision = __version__

    def canBeDeleted(self):
        """
        a object can be deleted with normal delete permission
        special objects can overload this for special delete rules
        (e.g. IAdmUtilCatHostGroup)
        return True or False
        """
        return len(self.isUsedIn()) == 0

    def isUsedIn(self):
        """
        this object is used at least in one host (returns object list)
        """
        retList = []
        for object in objectsWithInterface(IHost):
            if self.objectID in object.hostGroups:
                retList.append(object)
        utilXbar = getUtility(IAdmUtilEventCrossbar,
                              name='AdmUtilEventCrossbar')
        for (oid, obj) in utilXbar.items():
            if IAdmUtilEvent.providedBy(obj):
                if self.objectID == obj.hostGroup:
                    retList.append(obj)
        return retList
