# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0231,C0112,C0111
#
"""workflow logic for nagios interface
"""

__version__ = "$Id$"

# python imports
import os
from persistent import Persistent

# zope imports
from zope.location.location import Location
from zope.interface import implements
from zope.event import notify
from zope.wfmc import xpdl
from zope.wfmc import interfaces
from zope.wfmc.attributeintegration import AttributeIntegration
from zope.component import adapts, provideUtility

# ict_ok.org imports
from org.ict_ok.admin_utils.notifier.notifier import NotifyUserEvent

#path_splits = os.environ['PYTHONPATH'].split(':')
#for path_split in path_splits:
if os.path.exists('src/org/ict_ok/components/host/wf/host_nagios.xpdl'):
    xpdl_filename = 'src/org/ict_ok/components/host/wf/host_nagios.xpdl'
#    break

package = xpdl.read(open(xpdl_filename))


class Participant(Persistent):
    adapts(interfaces.IActivity)
    implements(interfaces.IParticipant)
    def __init__(self, activity):
        self.activity = activity
        self.worklist = []


class User:
    def __init__(self):
        self.work_list = []



pd = package[u'host_nagios1']
integration = AttributeIntegration()
pd.integration = integration


class ParticipantICT_Ok(Participant):
    def __init__(self, activity):
        Participant.__init__(self, activity)
integration.host_nagios1_par1Participant = ParticipantICT_Ok


class ParticipantNagios(Participant):
    def __init__(self, activity):
        Participant.__init__(self, activity)
integration.host_nagios1_par2Participant = ParticipantNagios

provideUtility(pd, name=pd.id)


#class IApplication(IWorkItem):
    #"""Defines a specific id for zope.wfmc.interfaces.IWorkItem objects."""


#class IAppHost_Init(IApplication):
    #"""
    #"""

class ApplicationBase(Persistent, Location):
    adapts(interfaces.IParticipant)
    implements(interfaces.IWorkItem)

    def __init__(self, participant):
        self.participant = participant
        self.activity = participant.activity
        self.process = participant.activity.process

    def start(self):
        wfd = self.participant.activity.process.workflowRelevantData
        hostObj = getattr(wfd, 'object')
        if self not in hostObj.wf_worklist:
            hostObj.wf_worklist.append(self)
            hostObj._p_changed = True

    def finish(self):
        wfd = self.participant.activity.process.workflowRelevantData
        hostObj = getattr(wfd, 'object')
        if self in hostObj.wf_worklist:
            hostObj.wf_worklist.remove(self)
            hostObj._p_changed = True
        self.participant.activity.workItemFinished(self)


class ICT_OkInitializeWorkItem(ApplicationBase):
    """ """
    def __init__(self, participant):
        ApplicationBase.__init__(self, participant)
    def start(self):
        #print "ICT_OkInitializeWorkItem.start"
        ApplicationBase.start(self)
        self.change()
    def change(self):
        self.finish()
    def finish(self):
        #print "ICT_OkInitializeWorkItem.finish"
        setattr(self.participant.activity.process.workflowRelevantData,
                "state", "initialized")
        ApplicationBase.finish(self)
integration.ict_ok_initializeWorkItem = ICT_OkInitializeWorkItem


class ICT_OkStartWorkItem(ApplicationBase):
    """ """
    def start(self):
        #print "ICT_OkStartWorkItem.start"
        setattr(self.participant.activity.process.workflowRelevantData,
                "new_state", "2_nagios_check")
        ApplicationBase.start(self)
        self.change()
    def change(self):
        self.finish()
    def finish(self):
        #print "ICT_OkStartWorkItem.finish"
        setattr(self.participant.activity.process.workflowRelevantData,
                "state", "started")
        ApplicationBase.finish(self)
integration.ict_ok_startWorkItem = ICT_OkStartWorkItem


class ICT_OkStopWorkItem(ApplicationBase):
    """ """
    def start(self):
        #print "ICT_OkStopWorkItem.start"
        ApplicationBase.start(self)
        self.change()
    def change(self):
        self.finish()
    def finish(self):
        #print "ICT_OkStopWorkItem.finish"
        setattr(self.participant.activity.process.workflowRelevantData,
                "state", "stopped")
        ApplicationBase.finish(self)
integration.ict_ok_stopWorkItem = ICT_OkStopWorkItem


class NagiosCheckWorkItem(ApplicationBase):
    """ """
    def start(self):
        #print "NagiosCheckWorkItem.start"
        setattr(self.participant.activity.process.workflowRelevantData,
                "state", "checking")
        setattr(self.participant.activity.process.workflowRelevantData,
                "new_state", "checking")
        ApplicationBase.start(self)
        self.change()
    def change(self):
        wfd = self.participant.activity.process.workflowRelevantData
        if getattr(wfd, 'state') != getattr(wfd, 'new_state'):
            self.finish()
    def finish(self):
        #print "NagiosCheckWorkItem.finish"
        ApplicationBase.finish(self)
integration.nagios_checkWorkItem = NagiosCheckWorkItem


class NagiosTriggerOnlineWorkItem(ApplicationBase):
    """ """
    def start(self):
        #print "NagiosTriggerOnlineWorkItem.start"
        setattr(self.participant.activity.process.workflowRelevantData,
                "state", "online")
        ApplicationBase.start(self)
        self.change()
    def change(self):
        wfd = self.participant.activity.process.workflowRelevantData
        if getattr(wfd, 'state') != getattr(wfd, 'new_state'):
            change_str = u"state changed: '%s' -> '%s'" % (wfd.state, wfd.new_state)
            hostObj = getattr(wfd, 'object')
            hostObj.appendHistoryEntry(change_str, level=u"warn")
            self.finish()
    def finish(self):
        #print "NagiosTriggerOnlineWorkItem.finish"
        setattr(self.participant.activity.process.workflowRelevantData,
                "state", "online")
        wfd = self.participant.activity.process.workflowRelevantData
        hostObj = getattr(wfd, 'object')
        notify(NotifyUserEvent(hostObj))
        ApplicationBase.finish(self)
integration.nagios_trigger_onlineWorkItem = NagiosTriggerOnlineWorkItem


class NagiosTriggerOfflineWorkItem(ApplicationBase):
    """ """
    def start(self):
        #print "NagiosTriggerOfflineWorkItem.start"
        setattr(self.participant.activity.process.workflowRelevantData,
                "state", "offline")
        ApplicationBase.start(self)
        self.change()
    def change(self):
        wfd = self.participant.activity.process.workflowRelevantData
        if getattr(wfd, 'state') != getattr(wfd, 'new_state'):
            change_str = u"state changed: '%s' -> '%s'" % (wfd.state, wfd.new_state)
            hostObj = getattr(wfd, 'object')
            hostObj.appendHistoryEntry(change_str, level=u"warn")
            self.finish()
    def finish(self):
        #print "NagiosTriggerOfflineWorkItem.finish"
        setattr(self.participant.activity.process.workflowRelevantData,
                "state", "offline")
        wfd = self.participant.activity.process.workflowRelevantData
        hostObj = getattr(wfd, 'object')
        notify(NotifyUserEvent(hostObj))
        ApplicationBase.finish(self)
integration.nagios_trigger_offlineWorkItem = NagiosTriggerOfflineWorkItem


class NagiosTriggerNotif1WorkItem(ApplicationBase):
    """ """
    def start(self):
        #print "NagiosTriggerNotif1WorkItem.start"
        setattr(self.participant.activity.process.workflowRelevantData,
                "state", "notification1")
        ApplicationBase.start(self)
        self.change()
    def change(self):
        wfd = self.participant.activity.process.workflowRelevantData
        if getattr(wfd, 'state') != getattr(wfd, 'new_state'):
            change_str = u"state changed: '%s' -> '%s'" % (wfd.state, wfd.new_state)
            hostObj = getattr(wfd, 'object')
            hostObj.appendHistoryEntry(change_str, level=u"warn")
            self.finish()
    def finish(self):
        #print "NagiosTriggerNotif1WorkItem.finish"
        setattr(self.participant.activity.process.workflowRelevantData,
                "state", "notification1")
        ApplicationBase.finish(self)
integration.nagios_trigger_notif1WorkItem = NagiosTriggerNotif1WorkItem
