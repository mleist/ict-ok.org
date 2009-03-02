# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: state.py 394 2009-01-06 15:12:30Z markusleist $
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of state-methods for PatchPort"""

__version__ = "$Id: state.py 394 2009-01-06 15:12:30Z markusleist $"

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.patchport.interfaces import IPatchPort
from org.ict_ok.components.supernode.interfaces import IState


class State(object):
    """Implementation of state adapter for Patch port
    """
    implements(IState)
    adapts(IPatchPort)


    def __init__(self, context):
        self.context = context

    def getStateValue(self):
        """get State-Value of the Object (0-100)
        """
        return 55

    def getStateOverview(self, parentOverviewNum=0):
        """get State-Overview of the Object (0: ok, 1: warn, 2: error)
        """
        linkCounter = len(self.context.links)
        overviewNum = parentOverviewNum # 0: ok, 1: warn, 2: error
        if linkCounter > 0:
            if overviewNum < 0:
                overviewNum = 0
        return overviewNum
