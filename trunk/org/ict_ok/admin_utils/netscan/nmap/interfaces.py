# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface to nmap scanner"""

__version__ = "$Id$"

# zope imports

# ict_ok.org imports
from org.ict_ok.admin_utils.netscan.interfaces import \
     IScanner


class IAdmUtilNMap(IScanner):
    """
    component for scanning network with nmap
    """
