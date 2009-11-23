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

# ict_ok.org imports
from org.ict_ok.admin_utils.idchooser.interfaces import \
    IAdmUtilIdChooser, IIdChooser
from org.ict_ok.components.supernode.supernode import Supernode


class AdmUtilIdChooser(Supernode):
    """Implementation of local id-getter/chooser Utility"""

    implements(IAdmUtilIdChooser)

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__

    def getIdChoosers(self):
        """ get all id chooser
        """
        idChoosers = []
        for (oid, obj) in self.items():
            if IIdChooser.providedBy(obj):
                idChoosers.append(obj)
        return idChoosers
