# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0612,W0232,W0142
#
"""implementation of browser class of Net object
"""

__version__ = "$Id$"

# phython imports

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

# zc imports
from zc.table.column import Column, GetterColumn
from zc.table.table import StandaloneFullFormatter
from zc.table.interfaces import ISortableColumn

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import IState
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import \
     IBrwsOverview, IEventIfSuperclass
from org.ict_ok.admin_utils.netscan.interfaces import INetScan
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditContent, EditForm
from org.ict_ok.components.net.interfaces import INet, IEventIfEventNet
from org.ict_ok.components.net.net import getAllNetworks, Net
from org.ict_ok.admin_utils.netscan.interfaces import \
     IScanner
from org.ict_ok.components.superclass.browser.superclass import \
     Overview, \
     getStateIcon, getTitel, getModifiedDate, getActionBottons, \
     raw_cell_formatter

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddNet(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Net')
    viewURL = 'add_net.html'
    weight = 50

# --------------- helper funktions -----------------------------

def getNetworkIp(item, formatter):
    """
    Ip for Overview
    """
    return item.ipv4

# --------------- object details ---------------------------


class NetDetails(ComponentDetails):
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
        if checkPermission('org.ict_ok.components.net.Add', self.context) and \
           (adapSize.sizeForSorting()[1] < 1):
            tmpDict = {}
            tmpDict['oid'] = u"c%sstart_scanner" % objId
            tmpDict['title'] = _(u"start scanner")
            tmpDict['href'] = u"%s/@@start_scanner.html" % \
                   zapi.getPath(self.context)
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
        #import pdb; pdb.set_trace()
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

# --------------- forms ------------------------------------


class DetailsNetForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of net')
    fields = field.Fields(INet).omit(*NetDetails.omit_viewfields)

class AddNetForm(AddForm):
    """Add form."""
    label = _(u'Add Net')
    fields = field.Fields(INet).omit(*NetDetails.omit_addfields)
    factory = Net


class EditNetForm(EditForm):
    """ Edit for for net """
    label = _(u'Net Edit Form')
    fields = field.Fields(INet).omit(*NetDetails.omit_editfields)
    
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


class DeleteNetForm(DeleteForm):
    """ Delete the net """
    
    def getTitel(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this net: '%s'?") % \
               IBrwsOverview(self.context).getTitle()

class EditNetEventIfForm(EditForm):
    """ Edit for for net """
    label = _(u'Net Event Interfaces Form')
    fields = field.Fields(IEventIfEventNet)


class AllNetworks(Overview):
    """Overview Pagelet"""
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Title'),
                     getter=getTitel),
        GetterColumn(title=_('Network'),
                     getter=getNetworkIp),
        GetterColumn(title=_('Modified On'),
                     getter=getModifiedDate,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    
    def objs(self):
        """List of Content objects"""
        return getAllNetworks()
    
    def table(self):
        """ Properties of table are defined here"""
        directlyProvides(self.columns[1], ISortableColumn)
        directlyProvides(self.columns[2], ISortableColumn)
        directlyProvides(self.columns[3], ISortableColumn)
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=self.columns, sort_on=((_('Title'), False),))
        formatter.cssClasses['table'] = 'listing'
        return formatter()


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
