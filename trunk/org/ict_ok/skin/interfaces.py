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
"""
skin interfaces
"""
__version__ = "$Id$"

# phython imports

# zope imports
from zope.viewlet.interfaces import IViewletManager

# z3c imports
from z3c.form.interfaces import IFormLayer
from z3c.formui.interfaces import ITableFormLayer
from z3c.layer.pagelet import IPageletBrowserLayer

class IBrowserLayer(IFormLayer, IPageletBrowserLayer):
    """Like IMinimalBrowserLayer including widget layer."""
    
class ISkin(ITableFormLayer, IBrowserLayer):
    """The browser skin."""

class IToolManager(IViewletManager):
    """Manager for tool viewlets."""

class IJavaScript(IViewletManager):
    """JavaScript viewlet manager."""
    
    
class IHeaders(IViewletManager):
    """Viewlets for the HTML header"""

class IToolbar(IViewletManager):
    """Viewlets for the toolbar (e.g. tabs and actions)"""

class IHd(IViewletManager):
    """Viewlets for the Gui-Header (e.g. version, breadcrums)"""

class IJsPre(IViewletManager):
    """Viewlets for the Javascript-Code pre content"""

class IJsPost(IViewletManager):
    """Viewlets for the Javascript-Code pre content"""

class IHdHelper(IViewletManager):
    """Viewlets for the Gui-Header (e.g. version, breadcrums)"""

class ISidebar(IViewletManager):
    """Viewlets for the sidebar (e.g. add menu)"""

class IFooter(IViewletManager):
    """Viewlets for the footer (e.g. colophon)"""

class INav(IViewletManager):
    """Viewlets for the Gui-Header (e.g. version, breadcrums)"""

class IMenu(IViewletManager):
    """Menu viewlet manager."""

class IMasterMenu(IViewletManager):
    """Master menu viewlet manager."""

class ISubMenu(IViewletManager):
    """Master menu viewlet manager."""
