# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611,R0201
#
"""Adapter implementation of state-methods
"""

__version__ = "$Id$"

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from zope.app.appsetup import appsetup

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor

_ = MessageFactory('org.ict_ok')


class State(object):
    """Implementation of state adapter for DummyContainer
    """
    implements(IState)
    adapts(IAdmUtilSupervisor)

    def __init__(self, context):
        self.context = context

    def getStateDict(self):
        """get the object state in form of a dict
        """
        overviewNum = 0 # 0: ok, 1: warn, 2: error
        warnList = []
        errorList = []
        retDict = {}
        if appsetup.getConfigContext().hasFeature('devmode'):
            if overviewNum < 1:
                overviewNum = 1
            mesg = _(u'Warning: ')
            mesg += _(u"in development mode")
            warnList.append(mesg)
        retDict['overview'] = ('ok', 'warn', 'error')[overviewNum]
        retDict['warnings'] = warnList
        retDict['errors'] = errorList
        if overviewNum == 0:
            return None
        return retDict
    