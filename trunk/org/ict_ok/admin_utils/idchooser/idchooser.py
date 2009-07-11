# -*- coding: utf-8 -*-
#
# Copyright (c) 2009
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
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# ict_ok.org imports
from org.ict_ok.admin_utils.idchooser.interfaces import \
    IAdmUtilIdChooser, IIdChooser
from org.ict_ok.components.supernode.supernode import Supernode


def AllIdChoosers(dummy_context):
    """Which host group are there
    """
    terms = []
    try:
        utilCategories = getUtility(IAdmUtilIdChooser)
        idChoosers = utilCategories.getIdChoosers()
        for idChooser in idChoosers:
            terms.append(SimpleTerm(idChooser.objectID,
                                    str(idChooser.objectID),
                                    idChooser.ikName))
        return SimpleVocabulary(terms)
    except ComponentLookupError, err:
        return SimpleVocabulary([])


class IdChooser(Supernode):
    """Implementation of host group entry."""

    implements(IIdChooser)

    wasUsed = FieldProperty(IIdChooser['wasUsed'])
    counter = FieldProperty(IIdChooser['counter'])
    step = FieldProperty(IIdChooser['step'])
    format = FieldProperty(IIdChooser['format'])
    
    def __init__(self, **data):
        """
        constructor of the object
        """
        Supernode.__init__(self, **data)
        for (name, value) in data.items():
            if name in IIdChooser.names():
                setattr(self, name, value)
        self.ikRevision = __version__

    def canBeDeleted(self):
        """
        a object can be deleted with normal delete permission
        special objects can overload this for special delete rules
        (e.g. IAdmUtilCatHostGroup)
        return True or False
        """
        return not self.wasUsed

    def incrementId(self):
        """return a unique valid id string.
        """
        self.wasUsed = True
        self.counter += self.step
        return self.format % self.counter
