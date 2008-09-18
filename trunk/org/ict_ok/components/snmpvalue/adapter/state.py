# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611,W0212
#
"""Adapter implementation of state-methods
"""

__version__ = "$Id$"

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.snmpvalue.interfaces import ISnmpValue


class State(object):
    """Implementation of state adapter for DummyContainer
    """
    implements(IState)
    adapts(ISnmpValue)


    def __init__(self, context):
        self.context = context

    def getStateValue(self):
        """get State-Value of the Object (0-100)
        """
        return 55
    
    def getIconName(self):
        """get the icon name of the object state
        """
        tmp_health = self.context.get_health()
        if tmp_health is None:
            return u"SNMP_gray.png"
        if tmp_health < 0.66666:
            if tmp_health < 0.33333:
                return u"SNMP_red.png"
            else:
                return u"SNMP_yel.png"
        else:
            return u"SNMP_green.png"
