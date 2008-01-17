# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0612,W0142
#
"""implementation of host object

host object represents a single computer system
this might be: server, switch, router, workstation, notebook etc
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

# ict_ok.org imports
from org.ict_ok.components.host.interfaces import IHost, IEventIfEventHost
from org.ict_ok.components.component import Component
from org.ict_ok.components.host.wf.nagios import pd as WfPdNagios
from org.ict_ok.admin_utils.wfmc.wfmc import AdmUtilWFMC


def AllHostGroups(dummy_context):
    """Which host group are there
    """
    terms = []
    for (gkey, gname) in {
        u'dns': u'name server',
        u'smtp': u'smtp-server'}.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)


class Host(Component):
    """
    the template instance
    """

    implements(IHost, IEventIfEventHost)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    hostname = FieldProperty(IHost['hostname'])
    manufacturer = FieldProperty(IHost['manufacturer'])
    vendor = FieldProperty(IHost['vendor'])
    hostGroup = FieldProperty(IHost['hostGroup'])
    workinggroup = FieldProperty(IHost['workinggroup'])
    hardware = FieldProperty(IHost['hardware'])
    user = FieldProperty(IHost['user'])
    inv_id = FieldProperty(IHost['inv_id'])
    room = FieldProperty(IHost['room'])
    osList = FieldProperty(IHost['osList'])
    url = FieldProperty(IHost['url'])
    url_type = FieldProperty(IHost['url_type'])
    url_authname = FieldProperty(IHost['url_authname'])
    url_authpasswd = FieldProperty(IHost['url_authpasswd'])
    console = FieldProperty(IHost['console'])
    genNagios = FieldProperty(IHost['genNagios'])
    
    eventInpObjs_shutdown = FieldProperty(\
        IEventIfEventHost['eventInpObjs_shutdown'])
    
    wf_pd_dict = {}
    wf_pd_dict[WfPdNagios.id] = WfPdNagios
    AdmUtilWFMC.wf_pd_dict[WfPdNagios.id] = WfPdNagios

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        # find our correct factory, is there a better solution?
        for (fact_name, fact_obj) in zapi.getFactoriesFor(IHost):
            if (len(fact_name) > 11) and (fact_name[:11]=='org.ict_ok.'):
                self.myFactory = unicode(fact_name)
        # initialize OS List
        self.osList = []
        self.eventInpObjs_shutdown = set([])
        for (name, value) in data.items():
            if name in IHost.names() or \
               name in IEventIfEventHost.names():
                setattr(self, name, value)
        self.ikRevision = __version__
        self.workflows[WfPdNagios.id] = nagios_wf = WfPdNagios()
        setattr(nagios_wf.workflowRelevantData, "ddd", 5)
        setattr(nagios_wf.workflowRelevantData, "state", "-")
        setattr(nagios_wf.workflowRelevantData, "object", self)
        setattr(nagios_wf.workflowRelevantData, "new_state", "2_start")
        nagios_wf.start()
        
    def trigger_online(self):
        """
        trigger workflow
        """
        print "trigger_online"
        lastWorkItem = list(self.wf_worklist)[-1]
        wfd = lastWorkItem.participant.activity.process.workflowRelevantData
        wfd.new_state = "online"
        lastWorkItem.change()

    def trigger_offline(self):
        """
        trigger workflow
        """
        print "trigger_offline"
        lastWorkItem = list(self.wf_worklist)[-1]
        wfd = lastWorkItem.participant.activity.process.workflowRelevantData
        wfd.new_state = "offline"
        lastWorkItem.change()

    def trigger_not1(self):
        """
        trigger workflow
        """
        print "trigger_not1"
        lastWorkItem = list(self.wf_worklist)[-1]
        wfd = lastWorkItem.participant.activity.process.workflowRelevantData
        wfd.new_state = "notification1"
        lastWorkItem.change()

    def eventInp_shutdown(self, eventMsg=None):
        """ start the shutdown of the host """
        eventMsg.stopit(self, "Host.eventInp_shutdown")
        print "Host.eventInp_shutdown (%s)       " \
        "       ############## <-" % (self.ikName)


def getAllHosts():
    """ get a list of all Hosts
    """
    retList = []
    uidutil = getUtility(IIntIds)
    for (myid, myobj) in uidutil.items():
        if IHost.providedBy(myobj.object):
            retList.append(myobj.object)
    return retList
