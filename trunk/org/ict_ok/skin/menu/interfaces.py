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
skin menu interfaces
"""
__version__ = "$Id$"

# python imports

# zope imports
from zope.viewlet.interfaces import IViewletManager

# z3c imports


class IMenu(IViewletManager):
    """Menu viewlet manager."""

class IMenuMain(IViewletManager):
    """Menu viewlet manager."""

class IMenuSub(IViewletManager):
    """Menu viewlet manager."""

class IMenuContext(IViewletManager):
    """Menu viewlet manager."""

class IMenuGeneral(IViewletManager):
    """Menu viewlet manager."""

class IMenuEvent(IViewletManager):
    """Menu viewlet manager."""

class IMenuScript(IViewletManager):
    """Menu viewlet manager."""

class IMenuAdmin(IViewletManager):
    """Menu viewlet manager."""
