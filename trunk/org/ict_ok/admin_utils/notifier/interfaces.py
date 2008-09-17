# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of Notifier-Utility"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.component.interfaces import IObjectEvent
from zope.schema import Choice, Set, List
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class INotifierUtil(ISupernode):
    """
    implementation of a "Notifier-Utility" 
    """
    
    notifierSet = List (
        title = _("Notifiers"),
        description = _("Which network notifiers should be triggerd"),
        value_type = Choice(
            title = _("Notifier"),
            vocabulary = "notifierInstances",),
            #values = [ u"nmap", u"kmap", u"omap"]),
        readonly = False,
        required = True)
    #notifierSet = Choice(
        #title = _("Notifier"),
        #vocabulary = "notifierInstances",
        #readonly = False,
        #required = True)
    
    def getAllNotifierObjs(self):
        """
        get list of all Notifier-Tupel (name, obj)
        """

    def getNotifierObjs(self):
        """
        get list of enabled Notifier-Tupel (name, obj)
        """

class INotifier(Interface):
    """
    component for notifying with
    """

class INotifyUserEvent(IObjectEvent):
    """A notification must be sent"""
