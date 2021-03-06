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
        self.notifierSet = []
        
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

    def send_test(self, messageText):
        """
        will send a test message by the notifier
        """
        print "NotifierUtil.send_test(%s)" % messageText
        notifiersList = self.getNotifierObjs()
        if notifiersList:
            for (name, obj) in notifiersList:
                obj.send_test(messageText)


class Notifier(Supernode):
    """implementation of a "Notifier-Utility" """

    implements(INotifier)

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__


class NotifyUserEvent(ObjectEvent):
    """A notification must be sent"""

    implements(INotifyUserEvent)

    def __init__(self, channels, level, arg_object) :
        """
        """
        super(NotifyUserEvent, self).__init__(arg_object)
        self.channels = channels
        self.level = level

def notifierInstances(dummy_context):
    """Which types of notifiers are there
    """
    utilList = [util for name, util in zapi.getUtilitiesFor(INotifier)]
    terms = [SimpleTerm(i.__name__, str(i.__name__), i.__name__) \
             for i in utilList]
    return SimpleVocabulary(terms)

errorLevel = 1000
warningLevel = 100
infoLevel = 10
allLevel = 0

def notifierLevels(dummy_context):
    terms = []
    for (gkey, gname) in {
        errorLevel: u"Error",
        warningLevel: u"Warning",
        infoLevel: u"Information",
        allLevel: u"All",
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

def notifierChannels(dummy_context):
    terms = []
    for (gkey, gname) in {
        u"ch_forecast": u"Forecast messages",
        u"ch_updown": u"Up and down messages",
        u"ch_misc": u"Miscellaneous messages",
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)
