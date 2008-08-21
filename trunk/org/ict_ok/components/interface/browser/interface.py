# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=F0401,E1101,E0611,W0232,W0142
#
"""implementation of browser class of Interface object
"""

__version__ = "$Id$"

# phython imports
from pysnmp.entity.rfc3413.oneliner import cmdgen
from datetime import datetime

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.dublincore.interfaces import IZopeDublinCore
from zope.traversing.browser import absoluteURL
from zope.lifecycleevent import ObjectCreatedEvent
from zope.event import notify
from zope.component import createObject

# z3c imports
from z3c.form import field
from z3c.pagelet.interfaces import IPagelet

# ict_ok.org imports
from org.ict_ok.components.interface.interfaces import IInterface, IInterfaceSnmpScanWizard
from org.ict_ok.components.interface.interface import Interface
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm, EditContent

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddInterface(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Interface')
    viewURL = 'add_interface.html'
    weight = 50


# --------------- object details ---------------------------


class InterfaceDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    #omit_viewfields = ComponentDetails.omit_viewfields + ['ipv4List']
    #omit_addfields = ComponentDetails.omit_addfields + ['ipv4List']
    #omit_editfields = ComponentDetails.omit_editfields + ['ipv4List']
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []

# --------------- forms ------------------------------------


class DetailsInterfaceForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of interface')
    fields = field.Fields(IInterface).omit(*InterfaceDetails.omit_viewfields)


class AddInterfaceForm(AddForm):
    """Add form."""
    label = _(u'Add Interface')
    fields = field.Fields(IInterface).omit(*InterfaceDetails.omit_addfields)
    factory = Interface


class EditInterfaceForm(EditForm):
    """ Edit for for net """
    label = _(u'Interface Edit Form')
    fields = field.Fields(IInterface).omit(*InterfaceDetails.omit_editfields)


class DeleteInterfaceForm(DeleteForm):
    """ Delete the net """
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this interface: '%s'?") % \
               IBrwsOverview(self.context).getTitle()

class SnmpScanWizardForm(AddForm):
    """Add form."""
    label = _(u'Search for IP?')
    fields = field.Fields(IInterfaceSnmpScanWizard)
    
    def getInterfaceCnt(self, data):
        searchIp = data['searchIpV4']
        hostObj = self.context
        snmpOid_IfNumber = (1, 3, 6, 1, 2, 1, 2, 1, 0)
        #import pdb
        #pdb.set_trace()
        try:
            hostSnmpVers = hostObj.snmpVersion
            hostSnmpPort = hostObj.snmpPort
            hostSnmpReadCommunity = hostObj.snmpReadCommunity
            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
                cmdgen.CommunityData('my-agent', hostSnmpReadCommunity, int(hostSnmpVers)),
                cmdgen.UdpTransportTarget((searchIp, hostSnmpPort, 5, 1)),
                snmpOid_IfNumber
            )
            return int(varBinds[0][1])
        except Exception, errText:
            print "Error in SnmpScanWizardForm.getInterfaceCnt: '%s'" % errText
            return None
        return None
    
    def getInterfaceVect(self, data, oidTuple):
        searchIp = data['searchIpV4']
        hostObj = self.context
        snmpOid_IfNumber = (1, 3, 6, 1, 2, 1, 2, 1, 0)
        try:
            hostSnmpVers = hostObj.snmpVersion
            hostSnmpPort = hostObj.snmpPort
            hostSnmpReadCommunity = hostObj.snmpReadCommunity
            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().nextCmd(
                cmdgen.CommunityData('my-agent', hostSnmpReadCommunity, int(hostSnmpVers)),
                cmdgen.UdpTransportTarget((searchIp, hostSnmpPort, 5, 1)),
                oidTuple
            )
            return varBinds
        except Exception, errText:
            print "Error in SnmpScanWizardForm.getInterfaceCnt: '%s'" % errText
            return None
        return None

    def nextURL(self):
        """ forward the browser """
        return absoluteURL(self.context, self.request)
    def create(self, data):
        print "SnmpScanWizardForm.create(%s)" % data
        interfaceCnt = self.getInterfaceCnt(data)
        if interfaceCnt and interfaceCnt > 0:
            interfacesDict = {}
            for i in range(0, interfaceCnt):
                interfacesDict[i] = {}
            oidTuple = (1, 3, 6, 1, 2, 1, 2, 2, 1, 1) # InterfaceIndex
            snmpList = self.getInterfaceVect(data, oidTuple)
            if snmpList:
                for snmpItem in snmpList:
                    interfacesDict[snmpList.index(snmpItem)]['index'] = \
                                  int(snmpItem[0][1])
            oidTuple = (1, 3, 6, 1, 2, 1, 2, 2, 1, 2) # InterfaceDesc
            snmpList = self.getInterfaceVect(data, oidTuple)
            if snmpList:
                for snmpItem in snmpList:
                    interfacesDict[snmpList.index(snmpItem)]['desc'] = \
                                  snmpItem[0][1].prettyPrint().strip("'")
            oidTuple = (1, 3, 6, 1, 2, 1, 2, 2, 1, 4) # InterfaceMtu
            snmpList = self.getInterfaceVect(data, oidTuple)
            if snmpList:
                for snmpItem in snmpList:
                    interfacesDict[snmpList.index(snmpItem)]['mtu'] = \
                                  int(snmpItem[0][1])
            oidTuple = (1, 3, 6, 1, 2, 1, 2, 2, 1, 5) # InterfaceSpeed
            snmpList = self.getInterfaceVect(data, oidTuple)
            if snmpList:
                for snmpItem in snmpList:
                    interfacesDict[snmpList.index(snmpItem)]['speed'] = \
                                  int(snmpItem[0][1])
            oidTuple = (1, 3, 6, 1, 2, 1, 2, 2, 1, 6) # InterfacehysAddress
            snmpList = self.getInterfaceVect(data, oidTuple)
            if snmpList:
                for snmpItem in snmpList:
                    interfacesDict[snmpList.index(snmpItem)]['mac'] = \
                                  "%02x:%02x:%02x:%02x:%02x:%02x" % \
                                  tuple([ord(i) for i in snmpItem[0][1]])
            oidTuple = (1, 3, 6, 1, 2, 1, 2, 2, 1, 7) # InterfaceAdminStatus
            snmpList = self.getInterfaceVect(data, oidTuple)
            if snmpList:
                for snmpItem in snmpList:
                    interfacesDict[snmpList.index(snmpItem)]['adminstat'] = \
                                  snmpItem[0][1] == 1
            oidTuple = (1, 3, 6, 1, 2, 1, 2, 2, 1, 8) # InterfaceOperStatus
            snmpList = self.getInterfaceVect(data, oidTuple)
            if snmpList:
                for snmpItem in snmpList:
                    interfacesDict[snmpList.index(snmpItem)]['operstat'] = \
                                  snmpItem[0][1] == 1
            oidTuple = (1, 3, 6, 1, 2, 1, 31, 1, 1, 1, 1) # InterfaceName
            snmpList = self.getInterfaceVect(data, oidTuple)
            if snmpList:
                for snmpItem in snmpList:
                    interfacesDict[snmpList.index(snmpItem)]['name'] = \
                                  snmpItem[0][1].prettyPrint().strip("'")
            # -------------------------------------------
            if data['indexType'] == u'index':
                atrList = [i['index'] for i in interfacesDict.values()]
                atrDict = {}.fromkeys(atrList)
                if len(atrDict.keys()) != interfaceCnt:
                    self.status = _(u"Error: interface index type 'Interface index' isn't unique")
                    return None
            elif data['indexType'] == u'mac':
                atrList = [i['mac'] for i in interfacesDict.values()]
                atrDict = {}.fromkeys(atrList)
                if len(atrDict.keys()) != interfaceCnt:
                    self.status = _(u"Error: interface index type 'Ethernet address' isn't unique")
                    return None
            elif data['indexType'] == u'desc':
                atrList = [i['desc'] for i in interfacesDict.values()]
                atrDict = {}.fromkeys(atrList)
                if len(atrDict.keys()) != interfaceCnt:
                    self.status = _(u"Error: interface index type 'Description' isn't unique")
                    return None
            elif data['indexType'] == u'name':
                atrList = [i['name'] for i in interfacesDict.values()]
                atrDict = {}.fromkeys(atrList)
                if len(atrDict.keys()) != interfaceCnt:
                    self.status = _(u"Error: interface index type 'Name' isn't unique")
                    return None
            # -------------------------------------------
            retList = []
            for interfaceKey in interfacesDict.keys()[:3]:
                tmpInterface = interfacesDict[interfaceKey]
                print "oooo:", tmpInterface
                dateNow = datetime.utcnow()
                newInterface = zapi.createObject(\
                    u'org.ict_ok.components.interface.interface.Interface')
                #notify(ObjectCreatedEvent(newInterface))
                newInterfaceDc = IZopeDublinCore(newInterface, None)
                newInterface.ikName = u"%s" % tmpInterface['desc']
                newInterfaceDc.title = u"%s" % tmpInterface['desc']
                newInterfaceDc.created = datetime.utcnow()
                newInterface.ikComment = u"%s" % tmpInterface['name']
                newInterface.mac = u"%s" % tmpInterface['mac']
                newInterface.ipv4List = None
                # -------------------------------
                #from org.ict_ok.components.snmpvalue.snmpvalue import SnmpValue
                #from org.ict_ok.components.superclass.interfaces import IBrwsOverview
                #from zope.app.keyreference.interfaces import IKeyReference
                #from zope.interface import directlyProvides
                #newSnmpvalue = zapi.createObject(\
                    #u'org.ict_ok.components.snmpvalue.snmpvalue.SnmpValue')
                ##directlyProvides(newSnmpvalue, IKeyReference)
                ##notify(ObjectCreatedEvent(newSnmpvalue))
                #newSnmpvalueDc = IZopeDublinCore(newSnmpvalue, None)
                #newSnmpvalueDc.title = u"%s" % "ddd"
                #newSnmpvalueDc.created = datetime.utcnow()
                #newSnmpvalue.__post_init__()
                ##data = {'ikName': u"ddd314"}
                ##obj = SnmpValue(**data)
                ##IBrwsOverview(obj).setTitle(data['ikName'])
                ##obj.__post_init__()
                ## -------------------------------
                #newInterface.__setitem__(u"ddd", newSnmpvalue)
                #newInterface.__setitem__(u"ddd", obj)
                newInterface.__post_init__()
                retList.append(newInterface)
            return retList
            # -------------------------------------------

        import pprint
        print "-" * 80
        pprint.pprint(interfacesDict)
        print "-" * 80
        #print "zzz: '%s'" % ddd
        #import pdb
        #pdb.set_trace()
        self.status = _(u"Error: no unique Id")
        return None #[1,2,3]
    def add(self, objList):
        """ will store the new one in object tree """
        print "SnmpScanWizardForm.add(%s)" % True #objList
        #import pdb
        #pdb.set_trace()
        for obj in objList:
            travp = self.context
            # store obj id for nextURL()
            self._newObjectID = obj.objectID
            while IPagelet.providedBy(travp):
                travp = self.context.__parent__
            travp[obj.ikName] = obj
            from org.ict_ok.components.snmpvalue.snmpvalue import SnmpValue
            #from org.ict_ok.components.superclass.interfaces import IBrwsOverview
            #from zope.app.keyreference.interfaces import IKeyReference
            #from zope.interface import directlyProvides
            #newSnmpvalue = zapi.createObject(\
                #u'org.ict_ok.components.snmpvalue.snmpvalue.SnmpValue')
            ###directlyProvides(newSnmpvalue, IKeyReference)
            #notify(ObjectCreatedEvent(newSnmpvalue))
            #newSnmpvalueDc = IZopeDublinCore(newSnmpvalue, None)
            #newSnmpvalueDc.title = u"%s" % "ddd"
            #newSnmpvalueDc.created = datetime.utcnow()
            #oid1 = SnmpOidValid(
            #oid2 = SnmpOidValid(
            #cmd = Choice(
            #inpMultiplier = Float(
            #inptype = Choice(
            #inpUnit = Choice(
            #displayUnitNumerator = Choice(
            #displayUnitDenominator = Choice(
            #checkMax = Bool(
            #checkMaxLevel = Int(
            #checkMaxLevelUnitNumerator = Choice(
            #checkMaxLevelUnitDenominator = Choice(
            #snmpIndexType = Choice(

            #newSnmpvalue.__post_init__()
            #newSnmpvalue = zapi.createObject(\
                #u'org.ict_ok.components.snmpvalue.snmpvalue.SnmpValue')
            ###directlyProvides(newSnmpvalue, IKeyReference)
            #notify(ObjectCreatedEvent(newSnmpvalue))
            data = {'ikName': u"ddd314",
                    'checktype': u"oid",
                    'oid1': u"1.3.6.1.2.1.1.1.0",
                    'oid2': u"1.3.6.1.2.1.1.1.0",
                    'cmd': u"none",
                    'inpMultiplier': 1.0,
                    'inptype': u"cnt",
                    'inpUnit': u"byte",
                    'displayUnitNumerator': u"Mbit",
                    'displayUnitDenominator': u"1",
                    'checkMax': False,
                    'checkMaxLevel': 100000,
                    'checkMaxLevelUnitNumerator': u"bit",
                    'checkMaxLevelUnitDenominator': u"1",
                    'snmpIndexType': u"index"
                    }
            newSnmpvalue = SnmpValue(**data)
            newSnmpvalueDc = IZopeDublinCore(newSnmpvalue, None)
            newSnmpvalueDc.title = u"%s" % "ddd"
            newSnmpvalueDc.created = datetime.utcnow()
            IBrwsOverview(newSnmpvalue).setTitle(data['ikName'])
            newSnmpvalue.__post_init__()
            # -------------------------------
            #newInterface.__setitem__(u"ddd", newSnmpvalue)
            obj.__setitem__(u"ddd", newSnmpvalue)
        #return objList
        #travp = self.context
        ## store obj id for nextURL()
        #self._newObjectID = obj.objectID
        #while IPagelet.providedBy(travp):
            #travp = self.context.__parent__
        #travp[obj.objectID] = obj
        return objList


#class AddForm(layout.FormLayoutSupport, form.AddForm):
    #"""Add form."""

    #form.extends(form.AddForm)
    #label = _(u'Add Superclass')
    #fields = field.Fields(ISuperclass).omit(\
        #*SuperclassDetails.omit_addfields)
    ## factory stores the class, which will instanciated in AddForm.create()
    #factory = Superclass

    #def nextURL(self):
        #""" forward the browser """
        #return absoluteURL(self.context[self._newObjectID],
                           #self.request)

    #def create(self, data):
        #""" will create the object """
        #obj = self.factory(**data)
        #IBrwsOverview(obj).setTitle(data['ikName'])
        #obj.__post_init__()
        #return obj
    
    #def add(self, obj):
        #""" will store the new one in object tree """
        #travp = self.context
        ## store obj id for nextURL()
        #self._newObjectID = obj.objectID
        #while IPagelet.providedBy(travp):
            #travp = self.context.__parent__
        #travp[obj.objectID] = obj
        #return obj
