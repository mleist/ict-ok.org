# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,E0211,W0232,W0622,C0103
#
"""Interface of EventCrossbar-Utility"""

__version__ = "$Id$"

# python imports
import datetime

# zope imports
from zope.interface import Attribute, Interface, Invalid, invariant
from zope.schema import Bool, Choice, Datetime, Set, TextLine, Timedelta
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import \
     IEventIfSupernode, ISupernode
from org.ict_ok.libs.lib import oid2dcTitle, nodeIsUnder

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
            vocabulary="AllObjectInstancesWithEventInputs"),
        default = set([]),
        readonly = False,
        required = True)

    hostGroup = Choice(
        title = _("host group"),
        vocabulary="AllHostGroups",
        readonly = False,
        required = False)

    location = Choice(
        title = _("Location"),
        description = _("The Location."),
        vocabulary="AllLocationsVocab",
        readonly = False,
        required = False)

    building = Choice(
        title = _("Building"),
        description = _("The Building."),
        vocabulary="AllBuildingsVocab",
        readonly = False,
        required = False)

    room = Choice(
        title = _("Room"),
        description = _("The Room Description."),
        vocabulary="AllRoomsVocab",
        readonly = False,
        required = False)

    @invariant
    def ensureRoomInBuilding(event):
        if event.room is not None and \
           event.building is not None and \
           not nodeIsUnder(event.room, event.building):
            raise Invalid(
                "Room '%s' is not in building '%s'." % \
                (oid2dcTitle(event.room), oid2dcTitle(event.building)))

    @invariant
    def ensureBuildingInLocation(event):
        if event.building is not None and \
           event.location is not None and \
           not nodeIsUnder(event.building, event.location):
            raise Invalid(
                "Building '%s' is not in location '%s'." % \
                (oid2dcTitle(event.building), oid2dcTitle(event.location)))
        
    @invariant
    def ensureRoomAtLocation(event):
        if event.room is not None and \
           event.location is not None and \
           not nodeIsUnder(event.room, event.location):
            raise Invalid(
                "Room '%s' is not in location '%s'." % \
                (oid2dcTitle(event.room), oid2dcTitle(event.location)))
        
    def addOidToInpObjects(oid):
        """ add oid to set """

    def addOidToOutObjects(oid):
        """ add oid to set """

    def removeOidFromInpObjects(oid):
        """ delete oid from set """

    def removeOidFromOutObjects(oid):
        """ delete oid from set """

    def removeInvalidOidFromInpOutObjects():
        """ delete all invalid oids """

class IAdmUtilEventCrossbar(ISupernode):
    """
    major component for registration and event distribution 
    """
    inpEQueues = Attribute("dict of input event queues")
    
    outEQueues = Attribute("dict of output event queues")

    def receiveEventCrossbar(str_time):
        """receive eventcrossbar signal
        """

    def getEventCrossbarTime():
        """get last eventcrossbar timestamp
        """
        
    def makeNewObjQueue(senderObj):
        """ will create a new input and output queue for this sender object """

    def destroyObjQueue(senderObj):
        """ will destroy the input and output queue for this sender object """

    def injectEventFromObj(senderObj, event):
        """ will inject an event from the sender object
        into the accordant queue """

    def getEvent(oidEventObject):
        """ will return the event with given oid or None """

    def tickerEvent():
        """ event """

    def debugEventHistory(eventObject):
        """ debug out the event history """


class IEventLogic(ISupernode):
    """
    superclass for any kind of 'logical' event objects
    """


class IEventIfEventLogic(IEventIfSupernode):
    """ event interface of object """


class IEventTimingRelay(IEventLogic):
    """
    timing relay with trigger- and reset-input and
    one delayed output
    """
    timeStart = Datetime(
        title = _("start time"),
        description = _("last trigger received at"),
        default = datetime.datetime(1901, 1, 1, 0, 0),
        readonly = True,
        required = False)
    timeDelta = Timedelta(
        title = _("delay time"),
        description = _("delayed time for output event"),
        default = datetime.timedelta(days=1),
        required = True)
    isRunning = Bool(
        title = _("timer is running"),
        default = False)


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
    def eventInp_trigger(eventMsg):
        """ start the timer """
    def eventInp_reset(eventMsg):
        """ reset the timer """
    def eventOut_1sec():
        """ sends one-second event """


class IEventTimer(IEventLogic):
    """
    timer with start- and stop-input and
    one pulse output
    """
    timeNext = Datetime(
        title = _("next pulse"),
        description = _("next pulse at"),
        default = datetime.datetime(1901, 1, 1, 0, 0),
        readonly = True,
        required = False)
    timePulse = Timedelta(
        title = _("pulse time"),
        description = _("pulse width for output event"),
        default = datetime.timedelta(seconds=60),
        required = True)
    isRunning = Bool(
        title = _("timer is running"),
        default = False)


class IEventIfEventTimer(IEventIfEventLogic):
    """ event interface of object """
    eventInpObjs_start = Set(
        title = _("start event <-"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)
    eventInpObjs_stop = Set(
        title = _("stop event <-"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)
    eventOutObjs_pulse = Set(
        title = _("pulse event ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)
    def eventInp_start(eventMsg):
        """ start the timer """
    def eventInp_stop(eventMsg):
        """ stop the timer """
    def eventOut_pulse():
        """ sends pulse event """


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
