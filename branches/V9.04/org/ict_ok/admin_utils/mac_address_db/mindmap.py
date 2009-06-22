# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <s.napiorkowski@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
"""Interface of mac address db util

the mac address db util will display some information from ict-ok in form of a mac address db
"""

__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# zc imports

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.mac_address_db.interfaces import \
     IAdmUtilMacAddressDb

logger = logging.getLogger("AdmUtilMacAddressDb")


class AdmUtilMacAddressDb(Supernode):
    """MacAddressDb Utiltiy
    """
    
    implements(IAdmUtilMacAddressDb)

    version = FieldProperty(IAdmUtilMacAddressDb['version'])
    
    def placeHolder(self):
        """ stupid place holder
        """
        return u"i'm not here"
