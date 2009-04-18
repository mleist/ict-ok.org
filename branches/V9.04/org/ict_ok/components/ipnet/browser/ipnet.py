# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: ipnet.py -1M 2009-04-17 06:22:56Z (lokal) $
#
# pylint: disable-msg=E1101,E0611,W0612,W0232,W0142
#
"""implementation of browser class of IpNet object
"""

__version__ = "$Id: ipnet.py -1M 2009-04-17 06:22:56Z (lokal) $"

# python imports

# zope imports
from zope.app import zapi
from zope.component import getUtility
from zope.size.interfaces import ISized
from zope.app.intid.interfaces import IIntIds
from zope.i18nmessageid import MessageFactory
from zope.security import checkPermission
from zope.app.catalog.interfaces import ICatalog
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import directlyProvides

# z3c imports
from z3c.form import button, field
from z3c.form.browser import checkbox

# zc imports
from zc.table.column import Column, GetterColumn
from zc.table.table import StandaloneFullFormatter
from zc.table.interfaces import ISortableColumn

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import \
     IBrwsOverview, IEventIfSuperclass
from org.ict_ok.admin_utils.netscan.interfaces import INetScan
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditContent, EditForm
from org.ict_ok.components.ipnet.interfaces import \
    IIpNet, IEventIfEventIpNet, IAddIpNet
from org.ict_ok.components.ipnet.ipnet import AllIpNets, IpNet
from org.ict_ok.admin_utils.netscan.interfaces import \
     IScanner
from org.ict_ok.components.superclass.browser.superclass import \
     Overview, \
     getStateIcon, getTitle, getModifiedDate, getActionBottons, getHealth, \
     raw_cell_formatter, IPsGetterColumn, TitleGetterColumn
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddIpNet(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add IpNet')
    viewURL = 'add_ipnet.html'
    weight = 50

# --------------- helper funktions -----------------------------

def getIpNetworkIp(item, formatter):
    """
    Ip for Overview
    """
    return item.ipv4

# --------------- object details ---------------------------


class IpNetDetails(ComponentDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    
    def actions(self):
        """
        gives us the action dict of the object
        """
        try:
            objId = getUtility(IIntIds).getId(self.context)
        except KeyError:
            objId = 1000
        retList = []
        adapSize = ISized(self.context)
        # adapSize.sizeForSorting() returns ('item', n)
        if checkPermission('org.ict_ok.components.host.Add', self.context) and \
           (adapSize.sizeForSorting()[1] < 1):
            tmpDict = {}
            tmpDict['oid'] = u"c%sstart_scanner" % objId
            tmpDict['title'] = _(u"start scanner")
            tmpDict['href'] = u"%s/@@start_scanner.html" % \
                   zapi.absoluteURL(self.context, self.request)
            tmpDict['tooltip'] = _(u"starts the network scanner (as user:%s)"\
                                   % self.request.principal.title)
            retList.append(tmpDict)
        #tmpDict = {}
        #tmpDict['oid'] = u"a%s" % objId
        #tmpDict['title'] = u"ich bin ein Titel"
        #tmpDict['href'] = u"http://www.essen.de"
        #tmpDict['tooltip'] = u"ich bin der \"aa\" 'bb' dazugehörige T"
        #retList.append(tmpDict)
        return retList

    def state(self):
        """
        gives us the state dict of the object
        """
        return IState(self.context).getStateDict()

    def start_scanner(self):
        """
        starts all configured scanners for this net
        """
        objNetScanner = getUtility(INetScan)
        if objNetScanner is not None:
            scannerList = objNetScanner.getScannerObjs()
            for (name, obj) in scannerList:
                obj.startScan(self.context)
        return self.request.response.redirect('./@@overview.html')
    
    def getDDD(self):
        """TODO: must check"""
        from org.ict_ok.admin_utils.supervisor.interfaces import \
             IAdmUtilSupervisor
        slaveSupervisor = zapi.queryUtility(IAdmUtilSupervisor,
                                            context=self.context)
        return slaveSupervisor.objectID
    

class IpNetFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
    attrInterface = IIpNet
    factory = IpNet
    fields = fieldsForFactory(factory, omit_editfields)

# --------------- forms ------------------------------------


class DetailsIpNetForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of net')
    factory = IpNet
    omitFields = IpNetDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

    
    
class AddIpNetForm(AddComponentForm):
    label = _(u'Add IpNet')
    factory = IpNet
    omitFields = IpNetDetails.omit_addfields
    attrInterface = IIpNet
    addInterface = IAddIpNet
    _session_key = 'org.ict_ok.components.ipnet'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditIpNetForm(EditForm):
    """ Edit for for net """
    label = _(u'IpNet Edit Form')
    factory = IpNet
    omitFields = IpNetDetails.omit_editfields
    fields = field.Fields(IIpNet).omit(*IpNetDetails.omit_editfields)
    fields = fieldsForFactory(factory, omitFields)
    fields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget

    ##TODO: Test-Button
    #@button.buttonAndHandler(u'test', name='test')
    #def handleApplyView(self, action):
        #self.handleApply(self, action)
        #my_catalog = zapi.getUtility(ICatalog)
        #ee=my_catalog[u'net_oid_index']
        #idUtil = getUtility(IIntIds)

        #for (oid) in ee.lexicon.words():
            #ointid = ee.index.search_phrase(oid).minKey()
            #oobj = idUtil.refs[ointid]
            #print "oobj: ", oobj
            ###print "ddd: ", (oid, idUtil.getObject(intid))


class DeleteIpNetForm(DeleteForm):
    """ Delete the net """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this net: '%s'?") % \
               IBrwsOverview(self.context).getTitle()

class EditIpNetEventIfForm(EditForm):
    """ Edit for for net """
    label = _(u'IpNet Event Interfaces Form')
    fields = field.Fields(IEventIfEventIpNet)


class AllIpNetworks(Overview):
    """Overview Pagelet"""
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Health'),
                     getter=getHealth),
        TitleGetterColumn(title=_('Title'),
                          getter=getTitle),
        IPsGetterColumn(title=_('IpNetwork'),
                        getter=getIpNetworkIp),
        GetterColumn(title=_('Modified'),
                     getter=getModifiedDate,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    sort_columns = [1, 2, 3, 4]
    
    def objs(self):
        """List of Content objects"""
        return AllIpNets()
    
    #def table(self):
        #""" Properties of table are defined here"""
        #directlyProvides(self.columns[1], ISortableColumn)
        #directlyProvides(self.columns[2], ISortableColumn)
        #directlyProvides(self.columns[3], ISortableColumn)
        #directlyProvides(self.columns[4], ISortableColumn)
        #formatter = StandaloneFullFormatter(
            #self.context, self.request, self.objs(),
            #columns=self.columns, sort_on=((_('Title'), False),))
        #formatter.cssClasses['table'] = 'listing'
        #return formatter()


def NetScannerInstances2(dummy_context):
    """Which types of network scanners are there
    """
    utilList = [util for name, util in zapi.getUtilitiesFor(IScanner)]
    utilList.sort()
    terms = [SimpleTerm(i.__name__, str(i.__name__), i.__name__) \
             for i in utilList]
    return SimpleVocabulary(terms)


def NamePrefixes(dummy_context=None):
    terms = []
    my_catalog = zapi.getUtility(ICatalog)
    ee=my_catalog[u'net_oid_index']
    idUtil = getUtility(IIntIds)
    # TODO dirty methode
    for (oid) in ee.lexicon.words():
        try:
            ointid = ee.index.search_phrase(oid).minKey()
            oobj = idUtil.refs[ointid]
            terms.append(SimpleTerm(oid, oobj.getDcTitle(), title=oobj.getDcTitle()))
        except ValueError:
            pass
    return SimpleVocabulary(terms)


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = IIpNet
    factory = IpNet
    factoryId = u'org.ict_ok.components.ipnet.ipnet.IpNet'
    allFields = fieldsForInterface(attrInterface, [])
