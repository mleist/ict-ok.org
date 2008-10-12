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
from zope.app.container.ordered import OrderedContainer

# ict_ok.org imports
from org.ict_ok.admin_utils.reports.interfaces import IAdmUtilReports
from org.ict_ok.components.superclass.superclass import Superclass


class AdmUtilReports(OrderedContainer, Superclass):
    """Implementation of local Reports-Utility"""

    implements(IAdmUtilReports)

    def __init__(self):
        Superclass.__init__(self)
        OrderedContainer.__init__(self)
        self.ikRevision = __version__
