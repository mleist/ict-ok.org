# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=F0401,E1101,E0611,W0612,W0232,W0201,W0142
#
"""implementation of browser class of IkSite object
"""

__version__ = "$Id$"

# python imports
import os
from datetime import datetime
import tempfile

# zope imports
from ZODB.interfaces import IConnection
from zope.security.proxy import removeSecurityProxy
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.security import checkPermission
from zope.app.rotterdam.xmlobject import setNoCacheHeaders

# zc imports

# gocept imports
from gocept.objectquery.pathexpressions import RPEQueryParser
from gocept.objectquery.processor import QueryProcessor

# ict-ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.version import getIkVersion
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     getUserTimezone
from org.ict_ok.components.supernode.browser.supernode import SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.reports.reports import AdmUtilReports
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.admin_utils.reports.reports import PDFReporter


_ = MessageFactory('org.ict_ok')


# --------------- helper functions -------------------------

# --------------- menu entries -----------------------------

class MSubReportNetworkPdf(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Network (PDF)')
    viewURL = '@@reportNetworkPdf.html'
    weight = 70

class MSubReportHardwarePdf(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Hardware (PDF)')
    viewURL = '@@reportHardwarePdf.html'
    weight = 71

class MSubReportSoftwarePdf(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Software (PDF)')
    viewURL = '@@reportSoftwarePdf.html'
    weight = 72

class MSubReportAllPdf(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All (PDF)')
    viewURL = '@@reportAllPdf.html'
    weight = 73

# --------------- object details ---------------------------

class AdmUtilReportsDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
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
        if checkPermission('org.ict_ok.admin_utils.reports.generate.pdf',
                           self.context):
            tmpDict = {}
            tmpDict['oid'] = u"c%sgenerate_test_pdf" % objId
            tmpDict['title'] = _(u"generate test pdf")
            tmpDict['href'] = u"%s/@@generate_test_pdf" % \
                   (zapi.absoluteURL(self.context, self.request))
            tmpDict['tooltip'] = _(u"will generate a test pdf file")
            retList.append(tmpDict)
        if checkPermission('org.ict_ok.admin_utils.reports.generate.pdf',
                           self.context):
            tmpDict = {}
            tmpDict['oid'] = u"c%sgenerate_all_pdf" % objId
            tmpDict['title'] = _(u"generate all pdf")
            tmpDict['href'] = u"%s/@@generate_all_pdf" % \
                   (zapi.absoluteURL(self.context, self.request))
            tmpDict['tooltip'] = _(u"will generate a all pdf file")
            retList.append(tmpDict)
        return retList

    def generateTestPdf(self):
        """
        will generate a test pdf file
        """
        filename = datetime.now().strftime('ictrpt_%Y%m%d%H%M%S.pdf')
        f_handle, f_name = tempfile.mkstemp(".pdf", filename)
        from org.ict_ok.admin_utils.reports import rpt_test01
        rpt_t01 = rpt_test01.RptTest01(f_name)
        rpt_t01.outPdf()
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

#    def reportNetworkPdf2(self):
#        filename = datetime.now().strftime('ictrpt_%Y%m%d%H%M%S.pdf')
#        f_handle, f_name = tempfile.mkstemp(filename)
#        authorStr = self.request.principal.title
#        my_formatter = self.request.locale.dates.getFormatter(
#            'dateTime', 'medium')
#        userTZ = getUserTimezone()
#        longTimeString = my_formatter.format(\
#            userTZ.fromutc(datetime.utcnow()))
#        versionStr = "%s [%s]" % (longTimeString, getIkVersion())
#        from ZODB.interfaces import IConnection
#        from zope.security.proxy import removeSecurityProxy
#        #import pdb
#        #pdb.set_trace()
#        connection = IConnection(removeSecurityProxy(self.context))
#        from gocept.objectquery.pathexpressions import RPEQueryParser
#        from gocept.objectquery.processor import QueryProcessor
#        parser = RPEQueryParser()
#        oc = connection.root()['_oq_collection']
##        # ---------------------------------------------------------
##        from zope.app import zapi
##        from org.ict_ok.components.superclass.interfaces import ISuperclass
##        iid = zapi.getUtility(IIntIds, '')
##        for (oid, oobj) in iid.items():
##            if ISuperclass.providedBy(oobj.object):
##                try:
##                    oc.index(oobj.object)
##                except AttributeError:
##                    pass
##                except TypeError:
##                    pass
##        # ---------------------------------------------------------
#        thisReporter = PDFReporter(f_name, self.request)
#        thisReporter.setAuthorName(authorStr)
#        thisReporter.setVersionStr(versionStr)
#        queryList = [
#                     ('HardwareAppliances', \
#                        '/Folder/HardwareApplianceFolder/HardwareAppliance'),
#                     ('Rooms', '/Folder/RoomFolder/Room'),
#                     ('Buildings', '/Folder/BuildingFolder/Building'),
#                     ('Locations', '/Folder/LocationFolder/Location'),
#                     ('Interfaces', '/Folder/InterfaceFolder/Interface'),
#                     ('OperatingSoftware', '/Folder/OperatingSoftwareFolder/OperatingSoftware'),
#                     ]
#        queryproc = QueryProcessor(parser, oc)
#        queryResultsList = [(queryn, queryproc(queryv))
#                            for (queryn, queryv) in queryList]
#        # first run
#        for (queryName, queryResults) in queryResultsList:
#            thisReporter.extendAllContentObjects(queryResults)
#        # second run
#        for (queryName, queryResults) in queryResultsList:
#            thisReporter.extendAllContentObjects(queryResults)
#            thisReporter.appendTitle1(queryName)
#            thisReporter.append(queryResults)
#
#        
##        ff=query('/Folder/HardwareApplianceFolder/HardwareAppliance')
##        gg=query('/Folder/RoomFolder/Room')
##        hh=query('/Folder/BuildingFolder/Building')
##        ii=query('/Folder/LocationFolder/Location')
###        ff2=query('/_*')
###        print "ff2: ", ff2
###        print "len(ff2): ", len(ff2)
##        thisReporter.extendAllContentObjects(ff)
##        thisReporter.extendAllContentObjects(gg)
##        thisReporter.extendAllContentObjects(hh)
##        thisReporter.extendAllContentObjects(ii)
###        thisReporter.extend(ff)
###        thisReporter.extend(gg)
###        thisReporter.extend(\
###            query('/Folder/BuildingFolder/Building'))
###        thisReporter.extend(\
###            query('/Folder/LocationFolder/Location'))
##        thisReporter.appendTitle1(u"/HardwareApplianceFolder/HardwareAppliance")
##        thisReporter.append(ff)
##        thisReporter.appendTitle1(u"/RoomFolder/Room")
##        thisReporter.append(gg)
##        thisReporter.appendTitle1(u"/BuildingFolder/Building")
##        thisReporter.append(hh)
##        thisReporter.appendTitle1(u"/LocationFolder/Location")
##        thisReporter.append(ii)
#
#
#        #thisReporter.allContentObjects.extend(ff2)
#        #thisReporter.fill()
#        thisReporter.buildPdf()
#        thisReporter.cleanup()
#        #self.context.generatePdf(f_name, authorStr, versionStr,request=self.request)
#
#        self.request.response.setHeader('Content-Type', 'application/pdf')
#        self.request.response.setHeader(\
#            'Content-Disposition',
#            'attachment; filename=\"%s\"' % filename)
#        setNoCacheHeaders(self.request.response)
#        datafile = open(f_name, "r")
#        dataMem = datafile.read()
#        datafile.close()
#        os.remove(f_name)
#        return dataMem

    def reportPdfByQueryList(self, queryList):
        filename = datetime.now().strftime('ictrpt_%Y%m%d%H%M%S.pdf')
        f_handle, f_name = tempfile.mkstemp(filename)
        authorStr = self.request.principal.title
        my_formatter = self.request.locale.dates.getFormatter(
            'dateTime', 'medium')
        userTZ = getUserTimezone()
        longTimeString = my_formatter.format(\
            userTZ.fromutc(datetime.utcnow()))
        versionStr = "%s [%s]" % (longTimeString, getIkVersion())
        connection = IConnection(removeSecurityProxy(self.context))
        parser = RPEQueryParser()
        oc = connection.root()['_oq_collection']
        thisReporter = PDFReporter(f_name, self.request)
        thisReporter.setAuthorName(authorStr)
        thisReporter.setVersionStr(versionStr)
        queryproc = QueryProcessor(parser, oc)
        queryResultsList = [(queryn, queryproc(queryv))
                            for (queryn, queryv) in queryList]
        # first run
        for (queryName, queryResults) in queryResultsList:
            thisReporter.extendAllContentObjects(queryResults)
        # second run
        for (queryName, queryResults) in queryResultsList:
            thisReporter.appendTitle1(queryName)
            thisReporter.append(queryResults)
        # debug output
        #for i_obj in thisReporter.allContentObjects:
        #    print "%s (%s)" % (i_obj.ikName, i_obj.objectID)
        thisReporter.buildPdf()
        thisReporter.cleanup()
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

    def reportNetworkPdf(self):
        queryList = [
                     ('HardwareAppliances', \
                        '/Folder/HardwareApplianceFolder/HardwareAppliance'),
                     ('Rooms', '/Folder/RoomFolder/Room'),
                     ('Buildings', '/Folder/BuildingFolder/Building'),
                     ('Locations', '/Folder/LocationFolder/Location'),
                     ('Interfaces', '/Folder/InterfaceFolder/Interface'),
                     ('OperatingSoftware', '/Folder/OperatingSoftwareFolder/OperatingSoftware'),
                     ]
        return self.reportPdfByQueryList(queryList)

    def reportHardwarePdf(self):
        queryList = [
                     ('HardwareAppliances', \
                        '/Folder/HardwareApplianceFolder/HardwareAppliance'),
                     ('Rooms', '/Folder/RoomFolder/Room'),
                     ('Buildings', '/Folder/BuildingFolder/Building'),
                     ('Locations', '/Folder/LocationFolder/Location'),
                     ]
        return self.reportPdfByQueryList(queryList)
    
    def reportSoftwarePdf(self):
        queryList = [
                     ('HardwareAppliances', \
                        '/Folder/HardwareApplianceFolder/HardwareAppliance'),
                     ('Rooms', '/Folder/RoomFolder/Room'),
                     ('Buildings', '/Folder/BuildingFolder/Building'),
                     ('Locations', '/Folder/LocationFolder/Location'),
                     ]
        return self.reportPdfByQueryList(queryList)
    
    def reportAllPdf(self):
        queryList = [
                     ('Application Software', '/Folder/ApplicationSoftwareFolder/ApplicationSoftware'),
                     ('Buildings', '/Folder/BuildingFolder/Building'),
                     ('Display Units', '/Folder/DisplayUnitFolder/DisplayUnit'),
                     ('Hardware Appliances', '/Folder/HardwareApplianceFolder/HardwareAppliance'),
                     ('Hosts', '/Folder/HostFolder/Host'),
                     ('Interfaces', '/Folder/InterfaceFolder/Interface'),
                     ('Ip Addresses', '/Folder/IpAddressFolder/IpAddress'),
                     ('Industrial Computers', '/Folder/IndustrialComputerFolder/IndustrialComputer'),
                     ('Ip Networks', '/Folder/IpNetFolder/IpNet'),
                     ('ISDN Phones', '/Folder/ISDNPhoneFolder/ISDNPhone'),
                     ('Latencies', '/Folder/LatencyFolder/Latency'),
                     ('Locations', '/Folder/LocationFolder/Location'),
                     ('Misc Physicals', '/Folder/MiscPhysicalFolder/MiscPhysical'),
                     ('Mobile Phones', '/Folder/MobilePhoneFolder/MobilePhone'),
                     ('Nets', '/Folder/NetFolder/Net'),
                     ('Notebooks', '/Folder/NotebookFolder/Notebook'),
                     ('Operating Software', '/Folder/OperatingSoftwareFolder/OperatingSoftware'),
                     ('Outlets', '/Folder/OutletFolder/Outlets'),
                     ('Patch Panels', '/Folder/PatchPanelFolder/PatchPanel'),
                     ('Patch Ports', '/Folder/PatchPortFolder/PatchPort'),
                     ('Personal Computers', '/Folder/PersonalComputerFolder/PersonalComputer'),
                     ('Physical Links', '/Folder/PhysicalLinkFolder/PhysicalLink'),
                     ('Printers', '/Folder/PrinterFolder/Printer'),
                     ('Racks', '/Folder/RackFolder/Rack'),
                     ('Rooms', '/Folder/RoomFolder/Room'),
                     ('Services', '/Folder/ServiceFolder/Service'),
                     ('Snmp Value', '/Folder/SnmpValueFolder/SnmpValue'),
                     ('Switches', '/Folder/SwitchFolder/Switch'),
                     ('X509 Certificates', '/Folder/X509CertificateFolder/X509Certificate'),
                     ]
        return self.reportPdfByQueryList(queryList)


# --------------- forms ------------------------------------

class DetailsAdmUtilReportsForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of reports')
    factory = AdmUtilReports
    omitFields = AdmUtilReportsDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

    
class EditAdmUtilReportsForm(EditForm):
    """ Edit for for net """
    label = _(u'edit report settings')
    factory = AdmUtilReports
    omitFields = AdmUtilReportsDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
