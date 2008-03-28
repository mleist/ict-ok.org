# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
#

#TODO Clean up

# phython imports

# zope imports
import zope.event
import zope.interface
from zope.wfmc import interfaces
from zope.interface import implements
from zope.wfmc import xpdl
from zope.app.appsetup import appsetup

lenDirName = len('etc/site.zcml') * -1
instDirName = appsetup.getConfigSource()[:lenDirName]
package = xpdl.read(open(instDirName + \
                         "lib/python/org/ict_ok/components/service/wf/service_nagios.xpdl"))

def log_workflow(event):
    print event
    
work_list = []

class Participant(object):
    zope.component.adapts(interfaces.IActivity)
    zope.interface.implements(interfaces.IParticipant)
    def __init__(self, activity):
        self.activity = activity
        #author_name = activity.process.workflowRelevantData.author
        #self.user = authors[author_name]

class User:
    def __init__(self):
        print "User:__init__"
        self.work_list = []



pd = package[u'service_nagios1']
from zope.wfmc.attributeintegration import AttributeIntegration
integration = AttributeIntegration()
pd.integration = integration

#integration.ICT_OkParticipant = Participant
integration.service_nagios1_par1Participant = Participant
integration.service_nagios1_par2Participant = Participant


import zope.component
zope.component.provideUtility(pd, name=pd.id)

class Publish:
    zope.component.adapts(interfaces.IParticipant)
    zope.interface.implements(interfaces.IWorkItem)

    def __init__(self, participant):
        print "Publish:__init__"
        self.participant = participant

    def start(self):
        print "Published"
        self.finish()

    def finish(self):
        self.participant.activity.workItemFinished(self)

class Initialize(Publish):
    def start(self):
        print "Initialize"
        self.finish()

integration.rejectWorkItem = Initialize

class service_nagios1_act1(Publish):
    def start(self):
        print "Start Service"
        self.finish()


from zope.wfmc.interfaces import IWorkItem

class IApplication(IWorkItem):
    """Defines a specific id for zope.wfmc.interfaces.IWorkItem objects."""

    #id = Int(
        #title=_(u'Id'),
        #description=_(u'Application (workitem) id.'),
        #required=False
        #)

    #def addStartedWorkitem():
        #"""Add started workitem to the WorkflowInformation annotation."""

    #def getObject():
        #"""Return the object (document)."""


class IAppService_Init(IApplication):
    """
    """


class ApplicationBase:
    zope.component.adapts(interfaces.IParticipant)
    zope.interface.implements(interfaces.IWorkItem)

    def __init__(self, participant):
        #print "ApplicationBase::__init__"
        self.participant = participant
        work_list.append(self)
        #participant.user.work_list.append(self)

    def start(self):
        print "ApplicationBase::start"
        pass

    def finish(self):
        print "ApplicationBase::finish"
        self.participant.activity.workItemFinished(self)


class service_nagios1_app1(ApplicationBase):
    """ """
    implements(IAppService_Init)
    def __init__(self, participant):
        #print "%%%%%%%%%%%% service_nagios1_app1::__init__(1)"
        self.process = participant.activity.process
        setattr(self.process.workflowRelevantData, 'transitionName', "-")
        #super(AppService_Init, self).__init__(participant)
        ApplicationBase.__init__(self, participant)
    def start(self, *arguments):
        #print "%%%%%%%%%%%% service_nagios1_app1::start(1)"
        self.addStartedWorkitem()
    def addStartedWorkitem(self):
        #print "%%%%%%%%%%%% service_nagios1_app1::addStartedWorkitem()"
        pass

integration.service_nagios1_app1 = service_nagios1_app1

class service_nagios1_app1WorkItem(ApplicationBase):
    """ """
    implements(IAppService_Init)
    def __init__(self, participant):
        #print "%%%%%%%%%%%% service_nagios1_app1WorkItem::__init__(1)"
        self.process = participant.activity.process
        setattr(self.process.workflowRelevantData, 'transitionName', "-")
        #super(AppService_Init, self).__init__(participant)
        ApplicationBase.__init__(self, participant)
    def start(self, *arguments):
        #print "%%%%%%%%%%%% service_nagios1_app1WorkItem::start(1)"
        self.addStartedWorkitem()
    def addStartedWorkitem(self):
        #print "%%%%%%%%%%%% service_nagios1_app1WorkItem::addStartedWorkitem()"
        pass

integration.service_nagios1_app1WorkItem = service_nagios1_app1WorkItem


proc = pd()

#print "----------->"
#print dir(pd)

from zope.component import queryUtility
from org.ict_ok.admin_utils.wfmc.interfaces import \
     IAdmUtilWFMC

utilWFMC = queryUtility(IAdmUtilWFMC)
#print "utilWFMC: %s" % utilWFMC

from zope.app import zapi
from org.ict_ok.admin_utils.objmq.interfaces import IAdmUtilObjMQ
mq_utility = zapi.queryUtility(IAdmUtilObjMQ)
#print "mq_utility: %s" % mq_utility

proc.start()

