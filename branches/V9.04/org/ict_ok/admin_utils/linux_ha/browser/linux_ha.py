# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232
#
"""implementation of browser class of linux_ha handler
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.interface import directlyProvides
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.security import checkPermission
from zope.i18nmessageid import MessageFactory

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter
from zc.table.interfaces import ISortableColumn

# z3c imports
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.admin_utils.linux_ha.linux_ha import \
     AdmUtilLinuxHa
from org.ict_ok.components.superclass.browser.superclass import \
     getActionBottons, getStateIcon, link, raw_cell_formatter, \
     DisplayForm, EditForm
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
#from org.ict_ok.admin_utils.linux_ha.linux_ha import globalLinuxHaUtility

_ = MessageFactory('org.ict_ok')

def getTitle(item, formatter):
    """
    Titel for Overview
    """
    try:
        if item.name:
            return u"%s" % item.name
        else:
            return None
    except AttributeError:
        return None


class AdmUtilLinuxHaDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_editfields = SupernodeDetails.omit_editfields + []

    def getInstanceCounter(self):
        """convert instance counter for display
        """
        return self.context.getInstanceCounter()

    def getLinuxHaTime(self):
        """convert linux_ha timestamp for display
        """
        return self.context.getLinuxHaTime()

    def getNodes(self):
        """ list view for all cluster nodes
        """
        return ["aa", "bb"].extend(self.context.getNodes())
    
    #def getGlobalLinuxHaUtility(self):
        #return globalLinuxHaUtility


class LinuxHaObjDetails(object):
    """ Class for Web-Browser-Details """
    displayName = u"Display: LinuxHaObjDetails"
    def getDisplayName(self):
        """ return Type of display class """
        return self.displayName

class LinuxHaDatacenterDetails(LinuxHaObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: LinuxHaDatacenterDetails"

class LinuxHaDatacentersDetails(LinuxHaObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: LinuxHaDatacentersDetails"

class LinuxHaDatastoreDetails(LinuxHaObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: LinuxHaDatastoreDetails"

class LinuxHaNetworkDetails(LinuxHaObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: LinuxHaNetworkDetails"

class LinuxHaFolderDetails(LinuxHaObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: LinuxHaFolderDetails"

class LinuxHaVirtualMachineDetails(LinuxHaObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: LinuxHaVirtualMachineDetails"
    
    def actions(self):
        """
        gives us the action dict of the object
        """
        try:
            objId = getUtility(IIntIds).getId(self.context)
        except KeyError:
            objId = 1000
        retList = []
        if checkPermission('org.ict_ok.admin_utils.linux_ha.Admin',
                           self.context) and\
           zapi.queryMultiAdapter((self.context, self.request),
                                  name='shutdown.html') is not None:
            tmpDict = {}
            tmpDict['oid'] = u"c%sshutdown" % objId
            tmpDict['title'] = _(u"shutdown")
            tmpDict['href'] = u"%s/@@shutdown.html?nextURL=%s" % \
                   (zapi.getPath( self.context),
                    quoter.quote())
            tmpDict['tooltip'] = _(u"shutdow the virtual machine")
            retList.append(tmpDict)
        if checkPermission('org.ict_ok.admin_utils.linux_ha.Admin',
                           self.context) and\
           zapi.queryMultiAdapter((self.context, self.request),
                                  name='convertobj.html') is not None:
            tmpDict = {}
            tmpDict['oid'] = u"c%sconvertobj" % objId
            tmpDict['title'] = _(u"convert to intern")
            tmpDict['href'] = u"%s/@@convertobj.html?nextURL=%s" % \
                   (zapi.getPath( self.context),
                    quoter.quote())
            tmpDict['tooltip'] = _(u"convert to internal object")
            retList.append(tmpDict)
        return retList

    def shutdown(self):
        """
        shutdown this esx object to an internal object
        """
        print("LinuxHaVirtualMachineDetails.shutdown")
        self.context.shutdown()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def convertobj(self):
        """
        converts this esx object to an internal object
        """
        print("LinuxHaVirtualMachineDetails.convertobj")
        r_obj = self.context.convertobj()
        return self.request.response.redirect(zapi.getPath(r_obj)+\
                                              '/@@details.html')
        #nextURL = self.request.get('nextURL', default=None)
        #if nextURL:
            #return self.request.response.redirect(nextURL)
        #else:
            #return self.request.response.redirect('./@@details.html')
        
        
class LinuxHaHostSystemDetails(LinuxHaObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: LinuxHaHostSystemDetails"

    
class Overview(BrowserPagelet):
    """Overview Pagelet"""
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Title'),
                     getter=getTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )

    def update(self):
        self.title = _(u"Overview Linux HA")

    def objs(self):
        """List of Content objects"""
        retList = []
        #self.context.connect2HaCluster()
        ##try:
            ##for obj in self.context.values():
                ##if ISuperclass.providedBy(obj):
                    ##retList.append(obj)
        ##except:
            ##pass
        for obj in self.context.values():
            #if ILinuxHaObj.providedBy(obj):
            retList.append(obj)
        return retList
        #return [obj
                #for obj in self.context.values()
                #if ISuperclass.providedBy(obj)]

    def table(self):
        """ Properties of table are defined here"""
        directlyProvides(self.columns[1], ISortableColumn)
        formatter = StandaloneFullFormatter(
            self.context, self.request, self.objs(),
            columns=self.columns, sort_on=((_('Title'), False),))
        formatter.cssClasses['table'] = 'listing'
        return formatter()

class OverviewLinuxHaDatacenters(Overview):
    """Overview Pagelet"""
    def update(self):
        self.title = _(u"Overview ESX VIM Datacenters")

class OverviewLinuxHaFolder(Overview):
    """Overview Pagelet"""
    def update(self):
        self.title = _(u"Overview ESX VIM %s" % self.context.name)

# --------------- forms ------------------------------------

class ViewAdmUtilLinuxHaForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of linux_ha')
    factory = AdmUtilLinuxHa
    omitFields = AdmUtilLinuxHaDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class EditAdmUtilLinuxHaForm(EditForm):
    """ Edit for for net """
    label = _(u'edit linux_ha')
    factory = AdmUtilLinuxHa
    omitFields = AdmUtilLinuxHaDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
