# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of size-methods
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.components.superclass.interfaces import IPickle
from org.ict_ok.components.superclass.adapter.ipickle import \
     Pickle as PickleSupernode

_ = MessageFactory('org.ict_ok')


class Pickle(PickleSupernode):
    """Pickle-Adapter."""

    implements(IPickle)
    adapts(IHost)

    def exportAsDict(self, mode='backup'):
        """
        this will export object properties as python-pickle
        """
        pickler = PickleSupernode(self.context)
        retVal = pickler.exportAsDict(mode)
        retVal['myFactory'] = self.context.myFactory
        retVal['listAttr']['revision'] = self.context.ikRevision
        retVal['listAttr']['myFactory'] = self.context.myFactory
        retVal['listAttr']['hostname'] = self.context.hostname
        retVal['listAttr']['manufacturer'] = self.context.manufacturer
        retVal['listAttr']['vendor'] = self.context.vendor
        retVal['listAttr']['workinggroup'] = self.context.workinggroup
        retVal['listAttr']['hardware'] = self.context.hardware
        retVal['listAttr']['user'] = self.context.user
        retVal['listAttr']['inv_id'] = self.context.inv_id
        retVal['listAttr']['room'] = self.context.room
        retVal['listAttr']['osList'] = osList = []
        for i in self.context.osList:
            osList.append(i)
        retVal['listAttr']['url'] = self.context.url
        retVal['listAttr']['url_type'] = self.context.url_type
        retVal['listAttr']['url_authname'] = self.context.url_authname
        retVal['listAttr']['url_authpasswd'] = self.context.url_authpasswd
        retVal['listAttr']['console'] = self.context.console
        retVal['listAttr']['genNagios'] = self.context.genNagios
        retVal['listAttr']['health'] = self.context.get_health()
        retVal['listAttr']['wcnt'] = self.context.get_wcnt()
        del pickler
        return retVal
