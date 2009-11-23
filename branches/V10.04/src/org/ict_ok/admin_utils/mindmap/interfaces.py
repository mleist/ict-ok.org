# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <s.napiorkowski@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0211,W0232,W0622
#
"""Interface of mind map util

the mind map util will display some information from ict-ok in form of a mind map
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.schema import Bool, TextLine
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class IAdmUtilMindMap(ISupernode):
    """MindMap Utiltiy
    """
    version = TextLine(
        title = _("mind map version"),
        description = _("mind maps must have a version."),
        readonly = False,
        required = False)

    cloudDisplay = Bool(
        title = _("Display Clouds"),
        description = _("Display Clouds"),
        default = False,
        required = False)

    def asMindmap(request=None):
        """ generate our mindmap root frame
        """
        
    def asMindmapData(request=None):
        """ generate our raw mindmap data
        """
