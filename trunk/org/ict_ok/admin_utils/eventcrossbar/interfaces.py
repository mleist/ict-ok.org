# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232,W0622,C0103
#
"""Interface of EventCrossbar-Utility"""

__version__ = "$Id$"

# python imports
from datetime import timedelta

# zope imports
from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, Set, TextLine, Timedelta
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class IAdmUtilEvent(ISupernode):
    """
    Interface auf an event which is distributed in event crossbar
    """
    title = TextLine(
        max_length = 40,
        title = _("event title"),
        description = _("Title of the event"),
        default = _("event_01"),
        required = True)
    
    logAllEvents = Bool(
        title = _("log events"),
        description = _("log all events"),
        default = False)
    
    inpObjects = Set(
        title = _("sender objects"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllObjectInstances"),
        default = set([]),
        readonly = False,
        required = True)
    
    outObjects = Set(
        title = _("receiver objects"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllObjectInstances"),
        default = set([]),
        readonly = False,
        required = True)

    def addOidToInpObjects(self, oid):
        """ delete oid from set """

    def addOidToOutObjects(self, oid):
        """ delete oid from set """

    def removeOidFromInpObjects(self, oid):
        """ delete oid from set """

    def removeOidFromOutObjects(self, oid):
        """ delete oid from set """

    def removeInvalidOidFromInpOutObjects(self):
        """ delete all invalid oids """


class IAdmUtilEventCrossbar(ISupernode):
    """
    major component for registration and event distribution 
    """
    inpEQueues = Attribute("dict of input event queues")
    
    outEQueues = Attribute("dict of output event queues")

    def receiveEventCrossbar(self, str_time):
        """receive eventcrossbar signal
        """

    def getEventCrossbarTime(self):
        """get last eventcrossbar timestamp
        """
        
    def makeNewObjQueue(self, senderObj):
        """ will create a new input and output queue for this sender object """

    def destroyObjQueue(self, senderObj):
        """ will destroy the input and output queue for this sender object """

    def injectEventFromObj(self, senderObj, event):
        """ will inject an event from the sender object
        into the accordant queue """

    def tickerEvent(self):
        """ event """


class IEventLogic(ISupernode):
    """
    superclass for any kind of 'logical' event objects
    """
    pass


class IEventIfEventLogic(IEventIfSupernode):
    """ event interface of object """
    pass


class IEventTimingRelay(IAdmUtilEventLogic):
    """
    timing relay with trigger- and reset-input and
    one delayed output
    """
    timeDelta = Timedelta(
        title = _("delay time"),
        description = _("delayed time for output event"),
        default = timedelta(0,60,0),
        required = True)


class IEventIfEventTimingRelay(IEventIfEventLogic):
    """ event interface of object """
    eventInpObjs_trigger = Set(
        title = _("trigger event <-"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)
    eventInpObjs_reset = Set(
        title = _("reset event <-"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)
    eventOutObjs_delayed = Set(
        title = _("delayed event ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)
    def eventInp_trigger(self):
        """ start the timer """
    def eventInp_reset(self):
        """ reset the timer """
    def eventOut_1sec(self):
        """ sends one-second event """


class IGlobalEventCrossbarUtility(Interface):
    """
    IGlobalEventCrossbarUtility
    """
    lastEventCrossbar = TextLine(
        min_length = 5,
        max_length = 40,
        title = _("Last EventCrossbar Start"),
        description = _("Date of last EventCrossbar-Start"),
        default = _("00.00.0000"),
        required = True)
