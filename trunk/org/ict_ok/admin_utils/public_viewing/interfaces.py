# -*- coding: utf-8 -*-
#
# Copyright (c) 2007,
#               Thomas Richter <thomas.richter at xwml.de>,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of PublicViewing-Utility"""

__version__ = "$Id$"

# zope imports

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode


class IAdmUtilPublicViewing(ISupernode):
    """
    major component for viewing by non authorized user
    """
    def getShadow(objId):
        """returns the public shadow object of the contentobject
        objId
        """

    def getAllShadows():
        """
        returns a list of all shadow objects
        """

