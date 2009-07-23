# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""implementation of a "linux ha node object" 
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.app.container.contained import Contained
from zope.app.container.interfaces import IReadContainer

# ict_ok.org imports
from org.ict_ok.libs.lib import generateOid
from org.ict_ok.admin_utils.linux_ha.interfaces import ILinuxHaObjNode


class LinuxHaObjNode(Contained):
    """
    """
    implements(ILinuxHaObjNode, IReadContainer)

    def __init__(self):
        Contained.__init__(self)
        self.objectID = generateOid(self)
        self.name = None

    def getObjectId(self):
        """
        get 'Universe ID' of object
        returns str
        """
        return self.objectID
