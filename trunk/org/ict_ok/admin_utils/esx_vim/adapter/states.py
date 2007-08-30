# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of esx vim state-methods
"""

__version__ = "$Id$"

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok imports
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.admin_utils.esx_vim.interfaces import IEsxVimObj



class State(object):
    """Implementation of state adapter for IkDummyContainer
    """
    implements(IState)
    adapts(IEsxVimObj)


    def __init__(self, context):
        self.context = context

    def getIconName(self):
        """get the icon name of the object state
        """
        if self.context.overallStatus == "gray":
            return u"ESX_gray.png"
        elif self.context.overallStatus == "green":
            return u"ESX_green.png"
        elif self.context.overallStatus == "red":
            return u"ESX_red.png"
        else:
            return u"Site_gr.png"
        return u"Site_gr.png"
