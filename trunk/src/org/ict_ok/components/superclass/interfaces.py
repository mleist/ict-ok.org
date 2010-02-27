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
"""Interface of Superclass"""

__version__ = "$Id$"

# zope imports
from zope.interface import Attribute, Interface
import zope.component.interfaces
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, List, Text, TextLine, Set, Object, Int
#from zope.mimetype.interfaces import IContentTypeAware

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
        max_length = 50,
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
    workflows = Attribute("dict of object workflows")
    wf_worklist = Attribute("list of ongoing workflow apps")
    shortName = Attribute("class shortname")

    def canBeDeleted():
        """
        a object can be deleted with normal delete permission
        special objects can overload this for special delete rules
        (e.g. IAdmUtilCatHostGroup)
        return True or False
        """
    def getObjectId():
        """
        get 'Universe ID' of object
        returns str
        """
    def setObjectId(arg_oid):
        """
        set 'Universe ID' of object
        only for backup/restore functions
        """
    def getShortname():
        """
        get a short class name of object
        returns str
        """
    def getParent():
        """
        returns parent object
        """
    def getDcTitle():
        """
        get the Title from Dublin Core
        """
    def setDcTitle(title):
        """
        set the Title to Dublin Core
        """
    def getModifiedTime():
        """
        get the modified time from Dublin Core
        """
    def appendHistoryEntry(entryText):
        """
        append an text entry to the history
        """
    def getAllOutEventObjs():
        """ returns a list of all active referenced event
        object oids for update purpose
        attribute name must start with 'eventOutObjs_'
        """
    def getAllInpEventObjs():
        """ returns a list of all active referenced event
        object oids for update purpose
        attribute name must start with 'eventInpObjs_'
        """
    def generatePdf(absFilename, authorStr, versionStr):
        """
        will generate a object pdf report
        """
    def generateXML(absFilename, authorStr, versionStr):
        """
        will generate a object XML report
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
    def triggerMin(self):
        """
        got ticker event from ticker thread every minute
        """
    def triggerHour(self):
        """
        got ticker event from ticker thread every hour
        """
    def triggerDay(self):
        """
        got ticker event from ticker thread every day
        """
    def triggerMonth(self):
        """
        got ticker event from ticker thread every month
        """
    def triggerYear(self):
        """
        got ticker event from ticker thread every year
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


class IFocus(Interface):
    """Interface for objects to display on focus-page
    """

class INavigation(Interface):
    """Interface for objects to display the navigation
    """
    def getContextObjList(preList=[], postList=[]):
        """
        get an Object list of all interesting objects in the context
        """

class IMsgEvent(Interface):
    """ Interface of an async event event
    """
    transmissionHistory = Attribute("objects which have seen this event")
    timeToLive = Attribute("hop count of routing objects")
    oidEventObject = Attribute("Oid from the Event message")
    targetFunctionName = Attribute("function name for lookup in receiver")
    # DontDoitFlag


class IEventIfSuperclass(Interface):
    """ event interface of object """

    #eventInpObjs_Ping = Set(
        #title = _("ping event <-"),
        #value_type = Choice(
            #title = _("objects"),
            #vocabulary="AllEventInstances"),
        #default = set([]),
        #readonly = False,
        #required = True)
    
    #eventOutObjs_Pong = Set(
        #title = _("pong event ->"),
        #value_type = Choice(
            #title = _("objects"),
            #vocabulary="AllEventInstances"),
        #default = set([]),
        #readonly = False,
        #required = True)
    
    #def eventInp_Ping(self):
        #""" trigger ping request in object """
    #def eventOut_Pong(self):
        #""" sends a ping response """

class IObjectAddedEvent(zope.component.interfaces.IObjectEvent):
    """An object has been created.

    The location will usually be ``None`` for this event."""
