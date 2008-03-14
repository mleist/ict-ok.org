# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=E0611
#
"""Configuration adapter for simple1-config files
"""

__version__ = "$Id$"

# phython imports
import logging

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.admin_utils.netscan.scanner import Scanner
from org.ict_ok.admin_utils.netscan.simple1.interfaces import IAdmUtilSimple1

logger = logging.getLogger("AdmUtilSimple1")


class AdmUtilSimple1(Scanner):
    """Implementation of simple1 scanner wrapper
    """

    implements(IAdmUtilSimple1)

    def __init__(self):
        super(AdmUtilSimple1, self).__init__()
        self.ikRevision = __version__
