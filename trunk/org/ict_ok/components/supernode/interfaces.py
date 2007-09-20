# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of Supernode"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.app.container.interfaces import IContainer
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import \
     IEventIfSuperclass, ISuperclass

# ict_ok.org imports
#from org.ict_ok.components.superclass.interfaces import ISuperclass

_ = MessageFactory('org.ict_ok')


class ISupernode(ISuperclass, IContainer):
    """A generator object."""

class IEventIfSupernode(IEventIfSuperclass):
    """ event interface of object """

class IState(Interface):
    """Interface of State-Adapter
    """
    def getStateValue(self):
        """get State-Value of the Object (0-100)
        """
    def getIconName(self):
        """get the icon name of the object state
        """
