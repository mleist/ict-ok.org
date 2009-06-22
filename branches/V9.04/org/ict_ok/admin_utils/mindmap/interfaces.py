# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <s.napiorkowski@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 88 2007-10-16 13:36:24Z markusleist $
#
# pylint: disable-msg=E0211,W0232,W0622
#
"""Interface of mind map util

the mind map util will display some information from ict-ok in form of a mind map
"""

__version__ = "$Id: interfaces.py_cog 88 2007-10-16 13:36:24Z markusleist $"

# python imports

# zope imports
from zope.schema import TextLine
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

    def placeHolder():
        """ stupid place holder
        """
