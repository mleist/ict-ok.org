# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611, W0612, R0201
#
"""Adapter implementation of size-methods
"""

__version__ = "$Id$"

# phython imports
from pickle import dumps

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from zope.security.proxy import removeSecurityProxy
from zope.xmlpickle import toxml

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass, IPickle

_ = MessageFactory('org.ict_ok')


class Pickle(object):
    """Pickle-Adapter."""

    implements(IPickle)
    adapts(ISuperclass)

    def __init__(self, context):
        self.context = context

    def exportAsDict(self, mode='backup'):
        """
        this will export object properties as python-pickle
        """
        retVal = {}
        retVal['objClass'] = self.context.__class__.__name__
        retVal['objName'] = self.context.__name__
        retVal['listAttr'] = {}
        retVal['listAttr']['ikName'] = self.context.ikName
        retVal['listAttr']['dbgLevel'] = self.context.dbgLevel
        retVal['listAttr']['objectID'] = self.context.objectID
        retVal['listAttr']['ikComment'] = self.context.ikComment
        retVal['listAttr']['ikAuthor'] = self.context.ikAuthor
        retVal['history'] = []
        print "exportAsDict - self.context.history: %s" % self.context.history
        if hasattr(self.context, 'history') and \
           self.context.history is not None:
            for entry in self.context.history:
                entry = removeSecurityProxy(entry)
                retVal['history'].append(entry.exportAsDict(mode))
        retVal['notes'] = []
        if hasattr(self.context, 'ikNotes') and \
           self.context.ikNotes is not None:
            for note in self.context.ikNotes:
                retVal['notes'].append(note)
        retVal['children'] = []
        for name, obj in self.context.items():
            recPickle = IPickle(obj)
            if recPickle:
                retVal['children'].append(recPickle.exportAsDict(mode))
        return retVal

    def convert2string(self, obj):
        """
        converts an object to an string
        """
        python_pickle = dumps(obj)
        return toxml(python_pickle)
