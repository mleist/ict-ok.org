# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
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

# python imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.folder import Folder

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.libs.lib import nodeIsUnder
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.host.interfaces import \
    IHost, IEventIfEventHost, IAddHost, IHostFolder
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.component import Component
from org.ict_ok.components.interfaces import \
    IImportCsvData, IImportXlsData
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.host.wf.nagios import pd as WfPdNagios
from org.ict_ok.admin_utils.wfmc.wfmc import AdmUtilWFMC
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IAdmUtilEventCrossbar
from org.ict_ok.components.logical_device.logical_device import LogicalDevice

#def AllHostGroups(dummy_context):
    #"""Which host group are there
    #"""
    #terms = []
    #for (gkey, gname) in {
        #u'dns': u'DNS-Server',
        #u'file': u'File-Server',
        #u'misc': u'Miscellaneous-Server',
        #u'smtp': u'SMTP-Server',
        #u'terminal': u'Terminal-Server',
        #u'util': u'Utility-Server',
        #u'workstation': u'Workstation',
        #}.items():
        #terms.append(SimpleTerm(gkey, str(gkey), gname))
    #return SimpleVocabulary(terms)

def getAllHosts():
    """ get a list of all Hosts
    """
    retList = []
    uidutil = getUtility(IIntIds)
    for (myid, myobj) in uidutil.items():
        if IHost.providedBy(myobj.object):
            retList.append(myobj.object)
    return retList

def AllHostProductionStates(dummy_context):
    """In which production state a host may be
    """
    terms = []
    for (gkey, gname) in {
        u'production': u'Production',
        u'preproduction': u'Pre-Production',
        u'test': u'Test',
        u'maintenance': u'Maintenance',
        u'decommissioned': u'Decommissioned',
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

def AllHosts(dummy_context):
    """In which production state a host may be
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if IHost.providedBy(oobj.object):
            myString = u"%s" % (oobj.object.getDcTitle())
            terms.append(\
                SimpleTerm(oobj.object,
                           token=getattr(oobj.object, 'objectID', oid),
                           title=myString))
    return SimpleVocabulary(terms)
    
def AllHostTemplates(dummy_context):
    """Which MobilePhone templates exists
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if IHost.providedBy(oobj.object) and \
        oobj.object.isTemplate:
            myString = u"%s [T]" % (oobj.object.getDcTitle())
            terms.append(SimpleTerm(oobj.object,
                                    token=getattr(oobj.object, 'objectID', oid),
                                    title=myString))
    return SimpleVocabulary(terms)



#Host_Interfaces_RelManager = FieldRelationManager(IHost['interfaces2'],
#                                                 IInterface['host2'],
#                                                 relType='host:interfaces')

class Host(LogicalDevice):
    """
    the template instance
    """

    implements(IHost, IEventIfEventHost)
    shortName = "host"
    # for ..Contained we have to:
    __name__ = __parent__ = None
    hostname = FieldProperty(IHost['hostname'])
#    manufacturer = FieldProperty(IHost['manufacturer'])
#    vendor = FieldProperty(IHost['vendor'])
#    hostGroups = FieldProperty(IHost['hostGroups'])
#    productionState = FieldProperty(IHost['productionState'])
#    workinggroup = FieldProperty(IHost['workinggroup'])
#    hardware = FieldProperty(IHost['hardware'])
#    user = FieldProperty(IHost['user'])
#    inv_id = FieldProperty(IHost['inv_id'])
#    room = FieldProperty(IHost['room'])
#    osList = FieldProperty(IHost['osList'])
#    snmpVersion = FieldProperty(IHost['snmpVersion'])
#    snmpPort = FieldProperty(IHost['snmpPort'])
#    snmpReadCommunity = FieldProperty(IHost['snmpReadCommunity'])
#    snmpWriteCommunity = FieldProperty(IHost['snmpWriteCommunity'])
#    url = FieldProperty(IHost['url'])
#    url_type = FieldProperty(IHost['url_type'])
#    url_authname = FieldProperty(IHost['url_authname'])
#    url_authpasswd = FieldProperty(IHost['url_authpasswd'])
#    console = FieldProperty(IHost['console'])
#    genNagios = FieldProperty(IHost['genNagios'])
    # Event interface
    eventInpObjs_shutdown = FieldProperty(\
        IEventIfEventHost['eventInpObjs_shutdown'])
    eventOutObjs_nagiosError = FieldProperty(\
        IEventIfEventHost['eventOutObjs_nagiosError'])
    
#    interfaces2 = RelationPropertyOut(Host_Interfaces_RelManager)
    
    wf_pd_dict = {}
    wf_pd_dict[WfPdNagios.id] = WfPdNagios
    AdmUtilWFMC.wf_pd_dict[WfPdNagios.id] = WfPdNagios

    def __init__(self, **data):
        """
        constructor of the object
        """
        LogicalDevice.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Host)
        # initialize OS List
        self.osList = []
        self.eventInpObjs_shutdown = set([])
        for (name, value) in data.items():
            if name in IHost.names() or \
               name in IEventIfEventHost.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__
        self.workflows[WfPdNagios.id] = nagios_wf = WfPdNagios()
        setattr(nagios_wf.workflowRelevantData, "ddd", 5)
        setattr(nagios_wf.workflowRelevantData, "state", "-")
        setattr(nagios_wf.workflowRelevantData, "object", self)
        setattr(nagios_wf.workflowRelevantData, "new_state", "2_start")
        nagios_wf.start()
        #health
        self._counter = {'r': 500}
        self._health = 1.0
        self._weight = {'r': 1.0}
        self._weight_user = 0.5

    def getRefAttributeNames(self):
        return getRefAttributeNames(Host)

    def store_refs(self, **data):
        LogicalDevice.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


    def trigger_online(self):
        """
        trigger workflow
        """
        #print "trigger_online"
        #self._counter['r'] += 10
        #print '$$$ self.get_health():', self.get_health()
        #print '$$$ self.get_wcnt():', self.get_wcnt()
        lastWorkItem = list(self.wf_worklist)[-1]
        wfd = lastWorkItem.participant.activity.process.workflowRelevantData
        wfd.new_state = "online"
        lastWorkItem.change()

    def trigger_offline(self):
        """
        trigger workflow
        """
        #print "trigger_offline"
        #self._counter['r'] -= 10
        #print '§§§ self.get_health():', self.get_health()
        #print '§§§ self.get_wcnt():', self.get_wcnt()
        #(Pdb) from z3c.form import datamanager
        #(Pdb) from z3c.form import term
        #(Pdb) dm1=datamanager.AttributeField(self, IHost['hostGroups'])
        #(Pdb) dm1.canAccess()
        #True
        #(Pdb) terms = term.ChoiceTerms(None, None, None, dm1.field.value_type, None)
        #(Pdb) terms.terms.getTerm(u'dcf0d4edda271cb4a1688501908fd298d').title
        #u'Miscellaneous-Server'
        #
        #(Pdb) from z3c.form import term
        #(Pdb) terms = term.ChoiceTerms(None, None, None, IHost['room'], None)
        #(Pdb) self.room
        #u'36301f822d5a62841d92a60f29f4df972'
        #(Pdb) terms.terms.getTerm(self.room)
        #<zope.schema.vocabulary.SimpleTerm object at 0x9f23210>
        #(Pdb) terms.terms.getTerm(self.room).title
        #u'Duisburg / RZ / Serverraum'
        
        lastWorkItem = list(self.wf_worklist)[-1]
        wfd = lastWorkItem.participant.activity.process.workflowRelevantData
        wfd.new_state = "offline"
        lastWorkItem.change()

    def trigger_not1(self):
        """
        trigger workflow
        """
        #print "trigger_not1"
        lastWorkItem = list(self.wf_worklist)[-1]
        wfd = lastWorkItem.participant.activity.process.workflowRelevantData
        wfd.new_state = "notification1"
        lastWorkItem.change()

    def inEventMask(self, eventMsg=None, testHostGroup=True):
        if eventMsg:
            utilXbar = getUtility(IAdmUtilEventCrossbar)
            if utilXbar is not None:
                origEvent = utilXbar.getEvent(eventMsg.oidEventObject)
                if origEvent is not None:
                    eventHostGroup = origEvent.hostGroup
                    eventLocation = origEvent.location
                    eventBuilding = origEvent.building
                    eventRoom = origEvent.room
                    # event for special hostgroup?
                    if testHostGroup and \
                       eventHostGroup is not None and \
                       len(eventHostGroup) > 0:
                        if not eventHostGroup in self.hostGroups:
                            return False
                    # event for special location
                    if eventLocation is not None and \
                       len(eventLocation) > 0:
                        if not nodeIsUnder(self.room, eventLocation):
                            return False
                    # event for special building
                    if eventBuilding is not None and \
                       len(eventBuilding) > 0:
                        if not nodeIsUnder(self.room, eventBuilding):
                            return False
                    # event for special room
                    if eventRoom is not None and \
                       len(eventRoom) > 0:
                        if self.room != eventRoom:
                            return False
                    return True
        return False
        
    def eventInp_shutdown(self, eventMsg=None):
        """ start the shutdown of the host """
        eventProcessed = False
        if self.inEventMask(eventMsg):
            eventProcessed = True
            #eventMsg.stopit(self, "Host.eventInp_shutdown")
            utilXbar = getUtility(IAdmUtilEventCrossbar)
            utilEvent = utilXbar[eventMsg.oidEventObject]
            if utilEvent.dryRun:
                print "Host.eventInp_shutdown (%s) (dry run)      " \
                "       ############## <-" % (self.ikName)
                print "eventMsg: ", eventMsg
            else:
                print "Host.eventInp_shutdown (%s)       " \
                "       ############## <-" % (self.ikName)
                print "eventMsg: ", eventMsg
        return eventProcessed
    
    def get_health(self):
        #return self._health
        stateAdapter = IState(self)
        stateNum = stateAdapter.getStateOverview(-1)
        if stateNum == 0:
            return 1.0
        elif stateNum == 1:
            return 0.5
        elif stateNum == 2:
            return 0.0
        else:
            return None
        return None

    def get_wcnt(self):
        """
        weighted count of accesses
        """
        wcnt = 0
        #net = zapi.getParent(self)
        for c_name, c_val in self._counter.items():
            #specifc counter * specific weight
            wcnt += self._weight[c_name]*c_val
        wcnt = wcnt * self._weight_user
        return int(wcnt)
    
    def getIpList(self):
        """ get a list of all possible ips
        """
        ipList = []
        for if_name, if_obj in self.items():
            if if_obj.ipv4List is not None:
                ipList.extend(if_obj.ipv4List)
        if len(ipList) > 0:
            return ipList
        else:
            return None


class HostFolder(Superclass, Folder):
    implements(IHostFolder, 
               IImportCsvData,
               IImportXlsData,
               IAddHost)
    def __init__(self, **data):
        """
        constructor of the object
        """
        Superclass.__init__(self, **data)
        Folder.__init__(self)
