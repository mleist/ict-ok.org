# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of state-methods for Switch"""

__version__ = "$Id$"

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.switch.interfaces import ISwitch
from org.ict_ok.components.supernode.interfaces import IState


class State(object):
    """Implementation of state adapter for Switch
    """
    implements(IState)
    adapts(ISwitch)


    def __init__(self, context):
        self.context = context

    def getStateValue(self):
        """get State-Value of the Object (0-100)
        """
        return 55
