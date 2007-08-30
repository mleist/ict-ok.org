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
"""Adapter implementation of state-methods
"""

__version__ = "$Id$"

# zope imports
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import IIKState
#from org.ict_ok.ikcodetemplate.interfaces import ICodetemplate


#class IKState(object):
    #"""Implementation of state adapter for DummyContainer
    #"""
    #implements(IIKState)
    #adapts(ICodetemplate)


    #def __init__(self, context):
        #self.context = context

    #def getStateValue(self):
        #"""get State-Value of the Object (0-100)
        #"""
        #return 55
