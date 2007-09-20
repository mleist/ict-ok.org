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
"""Interface of Superclass"""

__version__ = "$Id$"

# zope imports
from zope.interface import Attribute, Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, List, Text, TextLine, Set

# z3c imports
from z3c.reference.schema import ViewReferenceField

# ict_ok.org imports
from org.ict_ok.schema.objectidvalid import ObjectIdValid
#from org.ict_ok.components.supernode.interfaces import ISupernode

# ict_ok.org imports
#from org.ict_ok.schema.objectidvalid import ObjectIdValid

_ = MessageFactory('org.ict_ok')


class ISuperclass(Interface):
    """Interface for all Objects"""
    objectID = ObjectIdValid(
        title = _("Object id"),
        description = _("Oid of this object"),
        readonly = True,
        required = True)

    ikName = TextLine(
        min_length = 2,
        max_length = 40,
        title = _("Instance name"),
        description = _("Name of the instance."),
        required = True)

    ikAuthor = TextLine(
        max_length = 80,
        title = _("Instance author"),
        description = _("Author of the instance."),
        #default = _("Author"),
        required = False)

    ikNotes = List (
        title = _("Instance notes"),
        description = _("Notes for the instance " + \
                        "(in the context of using)."),
        value_type = Text(
            title = _("Instance note"),
            description = _("Note for the instance " + \
                            "(in the context of using)."),
            default = u""),
        readonly = False,
        required = False)

    ikComment = Text(
        title = _("Comment"),
        description = _("Comment for the instance " + \
                        "(in the context of installing)."),
        default = u"",
        required = False)
    
    ref = ViewReferenceField(
        title=u"Reference",
        required = False)
    
    history = Attribute("history list")
    dbgLevel = Attribute("Object Debug Level")
    ikEventTarget = Attribute("target list for events")
    inpEQueue = Attribute("input event queue")
    outEQueue = Attribute("output event queue")
    outEReceiver = Attribute("receiver object for output events")

    def getObjectId(self):
        """
        get 'Universe ID' of object
        returns str
        """
    def getDcTitle(self):
        """
        get the Title from Dublin Core
        """
    def setDcTitle(self, title):
        """
        set the Title to Dublin Core
        """
    def getAllOutEventObjs(self):
        """ returns a list of all active referenced event
        object oids for update purpose
        attribute name must start with 'eventOutObjs_'
        """
    def getAllInpEventObjs(self):
        """ returns a list of all active referenced event
        object oids for update purpose
        attribute name must start with 'eventInpObjs_'
        """


class IPickle(Interface):
    """Interface of Pickle-Adapter
    """
    def exportAsDict(self, mode):
        """
        exports self object as Python-Pickle
        """


class ITicker(Interface):
    """Interface of Ticker-Adapter
    will arrive every second
    """
    def triggered(self):
        """
        got ticker event from ticker thread
        """


class IBrwsOverview(Interface):
    """Interface of Title-Adapter
    """
    def getTitle(self):
        """
        get Title of the Object
        """

    def setTitle(self, title):
        """
        set Title of the Object
        """


class IMsgEvent(Interface):
    """ Interface of an async event event
    """
    transmissionHistory = Attribute("objects which have seen this event")
    timeToLive = Attribute("hop count of routing objects")
    oidEventObject = Attribute("Oid from the Event message")


class IEventIfSuperclass(Interface):
    """ event interface of object """

    eventInpObjs_Ping = Set(
        title = _("ping event <-"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)
    
    eventOutObjs_Pong = Set(
        title = _("pong event ->"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)
    
    def eventInp_Ping(self):
        """ trigger ping request in object """
    def eventOut_Pong(self):
        """ sends a ping response """
