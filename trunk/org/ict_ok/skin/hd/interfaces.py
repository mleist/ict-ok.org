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
"""
skin hd interfaces
"""
__version__ = "$Id$"

# phython imports

# zope imports
from zope.viewlet.interfaces import IViewletManager

# z3c imports


class IHd(IViewletManager):
    """Viewlets for the Gui-Header (e.g. version, breadcrums)"""

class IHdHelper(IViewletManager):
    """Viewlets for the Gui-Header (e.g. version, breadcrums)"""
