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
"""Adapter implementation of state-methods for PersonalComputer"""

__version__ = "$Id$"

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.pc.interfaces import IPersonalComputer
from org.ict_ok.components.supernode.interfaces import IState

_ = MessageFactory('org.ict_ok')


class State(object):
    """Implementation of state adapter for Personal Computer
    """
    implements(IState)
    adapts(IPersonalComputer)


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
#        obj = removeAllProxies(self.context)
#        owfs = obj.workflows
#        wfrd = owfs['host_nagios1'].workflowRelevantData
#        if wfrd.state == "offline":
        if True:
            if overviewNum < 1:
                overviewNum = 1
            mesg = _(u'Warning: ')
            mesg += _(u"'host is offline'")
            warnList.append(mesg)
#        if wfrd.state == "notification1":
#            if overviewNum < 2:
#                overviewNum = 2
#            mesg = _(u'Error: ')
#            mesg += _(u"'host is in notification1'")
#            warnList.append(mesg)
        retDict['overview'] = ('ok', 'warn', 'error')[overviewNum]
        retDict['warnings'] = warnList
        retDict['errors'] = errorList
        if overviewNum == 0:
            return None
        return retDict
