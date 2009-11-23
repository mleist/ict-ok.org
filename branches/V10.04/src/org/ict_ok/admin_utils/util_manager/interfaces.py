# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of utility manager"""

__version__ = "$Id$"

# zope imports

# ict_ok imports

# ict_ok.org imports
from zope.interface import Interface

# ict_ok imports


class IUtilManager(Interface):
    """
    major component for registration and event distribution in ICT_Ok
    """
