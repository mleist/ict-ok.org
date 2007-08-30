# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=
#
"""not specialized generator for configuration files
"""

__version__ = "$Id$"

# phython imports
import logging

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.netscan.interfaces import IScanner

logger = logging.getLogger("NetScan")


class Scanner(Supernode):
    """Implementation of unspecified generator
    """

    implements(IScanner)

    def __init__(self):
        Supernode.__init__(self)
