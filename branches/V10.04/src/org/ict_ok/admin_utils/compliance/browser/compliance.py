# -*- coding: utf-8 -*-
#
# Copyright (c) 2007, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
"""Interface of compliance utility

the compliance utility should store the compliance/requirement-templates
for the host- or service-instances

implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id$"

# python imports
import os
from datetime import datetime
import tempfile
from lxml import etree

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.security import checkPermission
from zope.app.rotterdam.xmlobject import setNoCacheHeaders
from zope.traversing.browser import absoluteURL

# zc imports
from zc.table.column import GetterColumn

# z3c imports
from z3c.form import button, field, form, interfaces
from z3c.formui import layout
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.version import getIkVersion
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     getUserTimezone
from org.ict_ok.admin_utils.compliance.interfaces import \
     IAdmUtilCompliance, IImportXmlData
from org.ict_ok.admin_utils.compliance.compliance import \
     AdmUtilCompliance
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.admin_utils.compliance.interfaces import IRequirement
from org.ict_ok.admin_utils.compliance.requirement import getRequirementList
from org.ict_ok.components.superclass.browser.superclass import \
     getActionBotton_Detail, getActionBotton_Edit, \
     getActionBotton_History, getActionBotton_Delete
from org.ict_ok.components.superclass.browser.superclass import \
     Overview, getModifiedDate, raw_cell_formatter, \
     link, getSize

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------

class MSubImportXmlData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Import XML Data')
    viewURL = 'importreqxmldata.html'
    weight = 290

class MSubExportXmlData(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Export XML Data')
    viewURL = 'exportreqxmldata.html'
    weight = 291


# --------------- details -----------------------------

class AdmUtilComplianceDetails(SupernodeDetails):
    """Compliance Utiltiy
    """
    
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    def actions(self):
        """
        gives us the action dict of the object
        """
        try:
            objId = getUtility(IIntIds).getId(self.context)
        except KeyError:
            objId = 1000
        retList = []
        if checkPermission('org.ict_ok.admin_utils.compliance.generate.pdf',
                           self.context):
            tmpDict = {}
            tmpDict['oid'] = u"c%sgenerate_all_pdf" % objId
            tmpDict['title'] = _(u"generate all pdf")
            tmpDict['href'] = u"%s/@@generate_all_pdf" % \
                   (zapi.absoluteURL(self.context, self.request))
            tmpDict['tooltip'] = _(u"will generate a all pdf file")
            retList.append(tmpDict)
        if checkPermission('org.ict_ok.admin_utils.compliance.Import',
                           self.context):
            tmpDict = {}
            tmpDict['oid'] = u"c%simport requirements" % objId
            tmpDict['title'] = _(u"import requirements")
            tmpDict['href'] = u"%s/@@import_requirements" % \
                   (zapi.absoluteURL(self.context, self.request))
            tmpDict['tooltip'] = _(u"will import requirements")
            retList.append(tmpDict)
        return retList
    

    def generateAllPdf(self):
        """
        will send the complete pdf report to the browser
        """
        filename = datetime.now().strftime('ictrpt_%Y%m%d%H%M%S.pdf')
        f_handle, f_name = tempfile.mkstemp(filename)
        authorStr = self.request.principal.title
        my_formatter = self.request.locale.dates.getFormatter(
            'dateTime', 'medium')
        userTZ = getUserTimezone()
        longTimeString = my_formatter.format(\
            userTZ.fromutc(datetime.utcnow()))
        versionStr = "%s [%s]" % (longTimeString, getIkVersion())
        self.context.generateAllPdf(f_name, authorStr, versionStr)
        self.request.response.setHeader('Content-Type', 'application/pdf')
        self.request.response.setHeader(\
            'Content-Disposition',
            'attachment; filename=\"%s\"' % filename)
        setNoCacheHeaders(self.request.response)
        datafile = open(f_name, "r")
        dataMem = datafile.read()
        datafile.close()
        os.remove(f_name)
        return dataMem

    def import_requirements(self):
        from org.ict_ok.admin_utils.compliance.bootstrap import \
             fillUtilitiyWithReqs
        fillUtilitiyWithReqs(self.context)
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def exportXmlData(self):
        """get xml file for all objects"""
        self.request.response.setHeader('Content-Type', 'application/x-ict-ok-data')
        self.request.response.setHeader(\
            'Content-Disposition',
            'attachment; filename=\"%s.xml\"' % self.context.objectID)
        setNoCacheHeaders(self.request.response)
        import pdb
        pdb.set_trace()
        return self.context.exportXmlData()

    def exportReqXmlData(self):
        """get xml file for all objects"""
        self.request.response.setHeader('Content-Type', 'application/x-ict-ok-data')
        self.request.response.setHeader(\
            'Content-Disposition',
            'attachment; filename=\"%s.xml\"' % self.context.objectID)
        setNoCacheHeaders(self.request.response)
        return self.context.exportReqXmlData()



# --------------- forms ------------------------------------


class DetailsAdmUtilComplianceForm(DisplayForm):
    """ Display form for the object """
    
    label = _(u'settings of Compliance')
    fields = field.Fields(IAdmUtilCompliance).omit(
       *AdmUtilComplianceDetails.omit_viewfields)

    def update(self):
        #my_catalog = zapi.getUtility(ICatalog)
        #vvvv = "eea46d598cb0448fcfad1bbb25d0342dd"
        #res = my_catalog.searchResults(oid_index=vvvv)
        #from zope.app.intid.interfaces import IIntIds
        #uidutil = getUtility(IIntIds)
        #for (myid, myobj) in uidutil.items():
            #print (myid, myobj.object)

        #if False:
            #from zope.component import adapts, queryUtility
            #from schooltool.requirement.interfaces import IScoreSystem
            #from zope.app.intid import IntIds
            #from zope.app.intid.interfaces import IIntIds
            #uu2 = queryUtility(IScoreSystem, "Comp_Pass/Fail")
            #uu3 = queryUtility(IIntIds)
            #from org.ict_ok.admin_utils.compliance.requirement import Requirement
            #from zope.proxy import removeAllProxies
            #obj = removeAllProxies(self.context)
            ##a1 = Requirement("a1")
            ##a2 = Requirement("a2")
            ##a3 = Requirement("a3")
            ##aa = Requirement("a")
            ##aa['a1'] = a1
            ##aa['a2'] = a2
            ##aa['a3'] = a3
            #managementOBJ = obj
            #try:
                #del managementOBJ['alle Requirements']
            #except KeyError:
                #pass
            #try:
                #del managementOBJ['IT-Sicherheitskonzept']
            #except KeyError:
                #pass
        DisplayForm.update(self)

def getActionBottons(item, formatter):
    """Action Buttons for Overview in Web-Browser
    """
    retHtml = u""
    retHtml += getActionBotton_Detail(item, formatter)
    retHtml += getActionBotton_Edit(item, formatter)
    retHtml += getActionBotton_History(item, formatter)
    retHtml += getActionBotton_Delete(item, formatter)
    return retHtml

def getTitle(item, formatter):
    """
    Titel for Overview
    """
    try:
        return item.ikName
    except TypeError:
        return str(item.__class__.__name__)


class AdmUtilRequirementDisplay(Overview):
    """for 1st level Requirements
    """
    label = _(u'display requirements')
    columns = (
        GetterColumn(title=_('Title'),
                     getter=getTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Size'),
                     getter=getSize,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    sort_columns = [0, 1]
    status = None
    
    def objs(self):
        """List of Content objects"""
        return [obj
                for obj in self.context.values()
                if IRequirement.providedBy(obj)]

class AdmUtilRequirementDisplayAll(AdmUtilRequirementDisplay):
    """for all Requirements
    """
    label = _(u'display all requirements')
    columns = (
        GetterColumn(title=_('Title'),
                     getter=getTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Modified'),
                     getter=getModifiedDate,
                     subsort=True,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Size'),
                     getter=getSize,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    pos_colum_index = 3
    sort_columns = [0, 1, 2]
    status = None
    def objs(self):
        """List of Content objects"""
        retList = []
        for reqObj in self.context.values():
            if IRequirement.providedBy(reqObj):
                retList.extend(getRequirementList(reqObj))
        return retList

class EditAdmUtilComplianceForm(EditForm):
    """ Display form for the object """
    
    label = _(u'edit Compliance properties')
    factory = AdmUtilCompliance
    omitFields = AdmUtilComplianceDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)

class ImportReqXmlDataForm(layout.FormLayoutSupport, form.Form):
    """ Delete the net """
    
    form.extends(form.Form)
    label = _(u"Import an 'all-data file' data")
    fields = field.Fields(IImportXmlData)
    
    @button.buttonAndHandler(u'Submit')
    def handleSubmit(self, action):
        """submit was pressed"""
        if 'alldata' in self.widgets:
            fileWidget=self.widgets['alldata']
            fileUpload = fileWidget.extract()
            #xml_string = ''.join(fileUpload.readlines())
            parser = etree.XMLParser(load_dtd=True,
                                     remove_blank_text=True)
            tree   = etree.parse(fileUpload, parser)
            print "--->", etree.tostring(tree.getroot(), pretty_print=True)
#
#            if self.context.importAllData(xml_string):
#                # ERROR behandlung
#                pass
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """cancel was pressed"""
        url = absoluteURL(self.context, self.request)
        self.request.response.redirect(url)

    def update(self):
        """update all widgets"""
        #if ISuperclass.providedBy(self.context):
            #self.label = self.getTitle()
        form.Form.update(self)
