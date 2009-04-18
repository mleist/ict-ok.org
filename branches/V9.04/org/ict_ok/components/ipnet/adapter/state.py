# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: state.py 425M 2009-04-16 11:09:07Z (lokal) $
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of state-methods
"""

__version__ = "$Id: state.py 425M 2009-04-16 11:09:07Z (lokal) $"

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.size.interfaces import ISized
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.ipnet.interfaces import IIpNet

_ = MessageFactory('org.ict_ok')


class State(object):
    """Implementation of state adapter for DummyContainer
    """
    implements(IState)
    adapts(IIpNet)


    def __init__(self, context):
        self.context = context

    def getStateValue(self):
        """get State-Value of the Object (0-100)
        """
        return 55
    
    def getStateDict(self):
        """get the object state in form of a dict
        """
        overviewNum = 0 # 0: ok, 1: warn, 2: error
        warnList = []
        errorList = []
        retDict = {}
        adapSize = ISized(self.context)
        # adapSize.sizeForSorting() returns ('item', n)
        if adapSize.sizeForSorting()[1] < 1:
            if overviewNum < 1:
                overviewNum = 1
            mesg = _(u'Warning: ')
            mesg += _(u"'no hosts in net'")
            warnList.append(mesg)
        retDict['overview'] = ('ok', 'warn', 'error')[overviewNum]
        retDict['warnings'] = warnList
        retDict['errors'] = errorList
        if overviewNum == 0:
            return None
        return retDict
