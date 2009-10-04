# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611,W0212
#
"""Adapter implementation of search-methods
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.index.text.interfaces import ISearchableText
from zope.i18nmessageid import MessageFactory
from zope.component import queryUtility

# ict_ok.org imports
from org.ict_ok.components.superclass.adapter.search import \
     Searchable as SuperSearchable
from org.ict_ok.components.interface.interfaces import \
     IInterface, convertIpV4
from org.ict_ok.components.interface.interface import Interface
from org.ict_ok.admin_utils.mac_address_db.interfaces import \
     IAdmUtilMacAddressDb

_ = MessageFactory('org.ict_ok')


class Searchable(SuperSearchable):
    """Searchable-Adapter."""

    implements(ISearchableText)
    adapts(IInterface)

    def __init__(self, context):
        SuperSearchable.__init__(self, context)

    def getSearchableInterfaceOid(self):
        """
        get Object id as string for catalog
        """
        return self.context.getObjectId()

#    def getSearchableInterfaceIp(self):
#        return convertIpV4(self.context.ipAddresses)

    def getSearchableInterfaceMac(self):
        return self.context.mac

    def getFullTextSearchFields(self):
        """
        """
        return Interface.fullTextSearchFields

    def getSearchableFullText(self):
        """
        get Object id as string for catalog
        """
        stringList = []
        for field in self.getFullTextSearchFields():
            #print u"%s : '%s'" % (field, getattr(self.context, field))
            stringList.append(u"%s" % getattr(self.context, field))
        macAddressDb = queryUtility(IAdmUtilMacAddressDb,
                                    name="AdmUtilMacAddressDb")
        if macAddressDb is not None:
            organization = macAddressDb.getOrganization(self.context.mac)
            if organization is not None:
                longString = organization['short']
                stringList.append(longString)
        return u" ".join(stringList)
