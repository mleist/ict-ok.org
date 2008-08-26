# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142,C0103
#
"""implementation of a "eventcrossbar daemon" 
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import queryUtility
from zope.app.catalog.interfaces import ICatalog

# ict_ok.org imports
from org.ict_ok.components.superclass.superclass import \
     isOidInCatalog, MsgEvent
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.eventcrossbar.interfaces import IAdmUtilEvent
from org.ict_ok.admin_utils.ticker.interfaces import IAdmUtilTicker
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar, IEventLogic


class AdmUtilEvent(Supernode):
    """Implementation of local EventCrossbar Utility"""

    implements(IAdmUtilEvent)
    
    title = FieldProperty(IAdmUtilEvent['title'])
    logAllEvents = FieldProperty(IAdmUtilEvent['logAllEvents'])
    dryRun = FieldProperty(IAdmUtilEvent['dryRun'])
    inpObjects = FieldProperty(IAdmUtilEvent['inpObjects'])
    outObjects = FieldProperty(IAdmUtilEvent['outObjects'])
    hostGroup = FieldProperty(IAdmUtilEvent['hostGroup'])
    location = FieldProperty(IAdmUtilEvent['location'])
    building = FieldProperty(IAdmUtilEvent['building'])
    room = FieldProperty(IAdmUtilEvent['room'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Supernode.__init__(self, **data)
        for (name, value) in data.items():
            if name in IAdmUtilEvent.names():
                setattr(self, name, value)
        self.ikRevision = __version__

    def addOidToInpObjects(self, oid):
        """ add oid to set """
        self.inpObjects.add(oid)

    def addOidToOutObjects(self, oidDotFct):
        """ add oid plus function name to set """
        self.outObjects.add(oidDotFct)

    def removeOidFromInpObjects(self, oid):
        """ delete oid from set """
        self.inpObjects.remove(oid)

    def removeOidFromOutObjects(self, oidDotFct):
        """ delete oid plus function name from set """
        self.outObjects.remove(oidDotFct)

    def removeInvalidOidFromInpOutObjects(self):
        """ delete all invalid oids 
        oids not in catalog will be deleted (exclude ticker)
        """
        utilTicker = queryUtility(IAdmUtilTicker)
        removeIDs = []
        for oid in self.inpObjects:
            if not isOidInCatalog(oid):
                removeIDs.append(oid)
        if utilTicker.getObjectId() in removeIDs:
            removeIDs.remove(utilTicker.getObjectId())
        for oid in removeIDs:
            self.inpObjects.remove(oid)
        removeIDs = []
        for oidPlusFunct in self.outObjects:
            oid = oidPlusFunct.split('.', 2)[0]
            if not isOidInCatalog(oid):
                removeIDs.append(oidPlusFunct)
        for oid in removeIDs:
            self.outObjects.remove(oid)

    def send_event(self,
                   logText=u"event triggered by call of send_event"):
        """ sends an the event to the list of ALL receivers
        """
        for oidPlusFunct in self.outObjects:
            oid = oidPlusFunct.split('.', 2)[0]
            # normal component objects
            my_catalog = zapi.getUtility(ICatalog)
            for resObj in my_catalog.searchResults(oid_index=oid):
                inst_event = MsgEvent(oidEventObject = self.objectID,
                                      logText=logText)
                resObj.injectInpEQueue(inst_event)
            # already in the above search results
            ## special event receivers
            #eventXbar = zapi.getUtility(IAdmUtilEventCrossbar, '')
            #for (i_oid, i_oobj) in eventXbar.items():
                #if IEventLogic.providedBy(i_oobj) and \
                   #i_oid == oid:
                    #print "2: ", i_oobj
                    #inst_event = MsgEvent(oidEventObject = self.objectID)
                    #i_oobj.injectInpEQueue(inst_event)
