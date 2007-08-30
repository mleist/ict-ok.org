# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232,W0622
#
"""Interface for general generator of configuration files
"""

__version__ = "$Id$"

# zope imports

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode


class IAdmUtilGenerators(ISupernode):
    """
    major component for registration and event distribution 
    """

