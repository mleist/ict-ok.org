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
from org.ict_ok.components.script.interfaces import IScript
from org.ict_ok.components.superclass.interfaces import IPickle
from org.ict_ok.components.supernode.adapter.ipickle import \
     Pickle as PickleSupernode

_ = MessageFactory('org.ict_ok')


class Pickle(PickleSupernode):
    """Pickle-Adapter."""

    implements(IPickle)
    adapts(IScript)

    def exportAsDict(self, mode='backup'):
        """
        this will export object properties as python-pickle
        """
        pickler = PickleSupernode(self.context)
        retVal = pickler.exportAsDict(mode)
        retVal['myFactory'] = self.context.myFactory
        retVal['listAttr']['pythonScript'] = self.context.pythonScript
        del pickler
        return retVal
