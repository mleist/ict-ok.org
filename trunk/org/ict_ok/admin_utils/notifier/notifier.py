# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612
#
"""implementation of a "Notifier-Utility" 
"""

__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.container.contained import Contained
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component.interfaces import ObjectEvent

# ict_ok imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.admin_utils.notifier.interfaces import INotifier
from org.ict_ok.admin_utils.notifier.interfaces import INotifierUtil
from org.ict_ok.admin_utils.notifier.interfaces import INotifyUserEvent

logger = logging.getLogger("Notifier")


class NotifierUtil(Supernode):
    """implementation of a "Notifier-Utility" """

    implements(INotifierUtil)

    notifierSet = FieldProperty(INotifierUtil['notifierSet'])

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__
        
    def getAllNotifierObjs(self):
        """
        get list of all Notifier-Tupel (name, obj)
        """
        return [(name, obj) for (name, obj) in \
                zapi.getUtilitiesFor(INotifier)]

    def getNotifierObjs(self):
        """
        get list of enabled Notifier-Tupel (name, obj)
        """
        if self.notifierSet:
            return [(name, obj) for (name, obj) \
                    in zapi.getUtilitiesFor(INotifier) \
                    if obj.__name__ in self.notifierSet]
        else:
            return None
    
    def sendNotify(self, notifyEvent=None, notifyObj=None):
        """
        send signal to all active notifiers
        """
        notifiersList = self.getNotifierObjs()
        if notifiersList:
            for (name, obj) in notifiersList:
                obj.sendNotify(notifyEvent, notifyObj)


class Notifier(Superclass, Contained):
    """implementation of a "Notifier-Utility" """

    implements(INotifier)

    def __init__(self):
        Superclass.__init__(self)
        Contained.__init__(self)
        self.ikRevision = __version__


class NotifyUserEvent(ObjectEvent):
    """A notification must be sent"""

    implements(INotifyUserEvent)

    def __init__(self, arg_object) :
        """
        """
        super(NotifyUserEvent, self).__init__(arg_object)

def notifierInstances(dummy_context):
    """Which types of notifiers are there
    """
    utilList = [util for name, util in zapi.getUtilitiesFor(INotifier)]
    terms = [SimpleTerm(i.__name__, str(i.__name__), i.__name__) \
             for i in utilList]
    return SimpleVocabulary(terms)
