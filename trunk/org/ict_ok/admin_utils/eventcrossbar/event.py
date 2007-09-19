# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""implementation of a "eventcrossbar daemon" 
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict_ok.org imports
from org.ict_ok.components.superclass.superclass import isOidInCatalog
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.eventcrossbar.interfaces import IAdmUtilEvent


class AdmUtilEvent(Supernode):
    """Implementation of local EventCrossbar Utility"""

    implements(IAdmUtilEvent)
    
    title = FieldProperty(IAdmUtilEvent['title'])
    inpObjects = FieldProperty(IAdmUtilEvent['inpObjects'])
    outObjects = FieldProperty(IAdmUtilEvent['outObjects'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Supernode.__init__(self, **data)
        for (name, value) in data.items():
            if name in IAdmUtilEvent.names():
                setattr(self, name, value)
        self.ikRevision = __version__

    def removeInvalidOidFromInpOutObjects(self):
        """ delete all invalid oids """
        removeIDs = []
        for oid in self.inpObjects:
            if not isOidInCatalog(oid):
                removeIDs.append(oid)
        for oid in removeIDs:
            self.inpObjects.remove(oid)
        removeIDs = []
        for oid in self.outObjects:
            if not isOidInCatalog(oid):
                removeIDs.append(oid)
        for oid in removeIDs:
            self.outObjects.remove(oid)
