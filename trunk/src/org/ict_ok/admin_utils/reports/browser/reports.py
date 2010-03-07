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
# Report Objects
from org.ict_ok.components.appsoftware.interfaces import IApplicationSoftware
from org.ict_ok.components.appsoftware.appsoftware import ApplicationSoftwareFolder
from org.ict_ok.components.building.interfaces import IBuilding
from org.ict_ok.components.display_unit.interfaces import IDisplayUnit
from org.ict_ok.components.group.interfaces import IGroup
from org.ict_ok.components.happliance.interfaces import IHardwareAppliance
from org.ict_ok.components.host.interfaces import IHost
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.ip_address.interfaces import IIpAddress
from org.ict_ok.components.ipc.interfaces import IIndustrialComputer
from org.ict_ok.components.ipnet.interfaces import IIpNet
from org.ict_ok.components.isdnphone.interfaces import IISDNPhone
from org.ict_ok.components.latency.interfaces import ILatency
from org.ict_ok.components.location.interfaces import ILocation
from org.ict_ok.components.misc_physical.interfaces import IMiscPhysical
from org.ict_ok.components.mobilephone.interfaces import IMobilePhone
from org.ict_ok.components.net.interfaces import INet
from org.ict_ok.components.notebook.interfaces import INotebook
from org.ict_ok.components.osoftware.interfaces import IOperatingSoftware
from org.ict_ok.components.outlet.interfaces import IOutlet
from org.ict_ok.components.patchpanel.interfaces import IPatchPanel
from org.ict_ok.components.patchport.interfaces import IPatchPort
from org.ict_ok.components.pc.interfaces import IPersonalComputer
from org.ict_ok.components.physical_link.interfaces import IPhysicalLink
from org.ict_ok.components.physical_media.interfaces import IPhysicalMedia
from org.ict_ok.components.printer.interfaces import IPrinter
from org.ict_ok.components.rack.interfaces import IRack
from org.ict_ok.components.role.interfaces import IRole
from org.ict_ok.components.room.interfaces import IRoom
from org.ict_ok.components.service.interfaces import IService
from org.ict_ok.components.snmpvalue.interfaces import ISnmpValue
from org.ict_ok.components.switch.interfaces import ISwitch
from org.ict_ok.components.x509certificate.interfaces import IX509Certificate
from org.ict_ok.components.product.interfaces import IProduct
from org.ict_ok.components.product.product import \
    getFirstLevelObjectList as getFirstLevelProductList
from org.ict_ok.components.address.interfaces import IAddress
from org.ict_ok.components.organization.interfaces import IOrganization
from org.ict_ok.components.person.interfaces import IPerson
from org.ict_ok.components.contact.interfaces import IContact
from org.ict_ok.components.contact_item.interfaces import IContactItem
from org.ict_ok.components.work_order.interfaces import IWorkOrder


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

class MSubReportPersonsPdf(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Persons (PDF)')
    viewURL = '@@reportPersonsPdf.html'
    weight = 101

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
        print "xX-" * 30
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
#            thisReporter.appendHeading1(queryName)
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
##        thisReporter.appendHeading1(u"/HardwareApplianceFolder/HardwareAppliance")
##        thisReporter.append(ff)
##        thisReporter.appendHeading1(u"/RoomFolder/Room")
##        thisReporter.append(gg)
##        thisReporter.appendHeading1(u"/BuildingFolder/Building")
##        thisReporter.append(hh)
##        thisReporter.appendHeading1(u"/LocationFolder/Location")
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
        import pdb
        pdb.set_trace()
        queryResultsList = [(queryn, queryproc(queryv))
                            for (queryn, queryv) in queryList]
        # first run
        for (queryName, queryResults) in queryResultsList:
            thisReporter.extendAllContentObjects(queryResults)
        # second run
        for (queryName, queryResults) in queryResultsList:
            thisReporter.appendHeading1(queryName)
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

    def reportPdfByObjectList(self, objsList, title=_(u'Report')):
        """
        generate a report from oll container-objects in objsList
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
        thisReporter = PDFReporter(f_name, self.request)
        thisReporter.setAuthorName(authorStr)
        thisReporter.setVersionStr(versionStr)
        # first run
        for (queryName, queryResults) in objsList:
            thisReporter.extendAllContentObjects(queryResults)
        from org.ict_ok.admin_utils.reports.interfaces import IAdmUtilReports
        utilAdmReports = getUtility(IAdmUtilReports, name='AdmUtilReports')
        thisReporter.appendTitle(title)
        thisReporter.appendVSpace(0.7)
        thisReporter.appendPara(_(u'Company') + u':')
        thisReporter.appendVSpace(0.7)
        if utilAdmReports.operatingCompany is not None:
            operatingCompany = utilAdmReports.operatingCompany
            if operatingCompany.adresses is not None and \
                len(operatingCompany.adresses) > 0:
                firstAddress = operatingCompany.adresses[0]
                thisReporter.appendPara(u'%s' % operatingCompany.ikName)
                if firstAddress.address1 is not None:
                    thisReporter.appendPara(u'%s' % firstAddress.address1 )
                if firstAddress.address2 is not None:
                    thisReporter.appendPara(u'%s' % firstAddress.address2 )
                if firstAddress.address3 is not None:
                    thisReporter.appendPara(u'%s' % firstAddress.address3 )
                if firstAddress.postalCode is not None:
                    thisReporter.appendPara(u'%s %s' % (firstAddress.postalCode, firstAddress.city))
                if firstAddress.country is not None:
                    thisReporter.appendPara(u'%s' % firstAddress.country )
        thisReporter.appendVSpace(0.7)
        thisReporter.appendToc()
        # second run
        for (queryName, queryResults) in objsList:
            thisReporter.appendHeading1(queryName)
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



    def _makeObjectList(self, interf, foldername):
        uidutil = getUtility(IIntIds)
        i_list = [oobj.object for (oid, oobj) in uidutil.items() \
                  if interf.providedBy(oobj.object)]
        i_list.sort(cmp=lambda x,y: x.ikName < y.ikName)
        if len(i_list) > 0:
            return [(foldername, i_list)]
        else:
            return []
    
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
        uidutil = getUtility(IIntIds)
        objsList = []
        objsList.extend(self._makeObjectList(IApplicationSoftware,
                                             _(u'Application Software')))
        objsList.extend(self._makeObjectList(IBuilding,
                                             _(u'Buildings')))
        objsList.extend(self._makeObjectList(IDisplayUnit,
                                             _(u'Display Units')))
        objsList.extend(self._makeObjectList(IHardwareAppliance,
                                             _(u'Hardware Appliances')))
        objsList.extend(self._makeObjectList(IHost,
                                             _(u'Hosts')))
        objsList.extend(self._makeObjectList(IInterface,
                                             _(u'Interfaces')))
        objsList.extend(self._makeObjectList(IIpAddress,
                                             _(u'Ip Addresses')))
        objsList.extend(self._makeObjectList(IIndustrialComputer,
                                             _(u'Industrial Computers')))
        objsList.extend(self._makeObjectList(IIpNet,
                                             _(u'Ip Networks')))
        objsList.extend(self._makeObjectList(IISDNPhone,
                                             _(u'ISDN Phones')))
        objsList.extend(self._makeObjectList(ILatency,
                                             _(u'Latencies')))
        objsList.extend(self._makeObjectList(ILocation,
                                             _(u'Locations')))
        objsList.extend(self._makeObjectList(IMiscPhysical,
                                             _(u'Misc Physicals')))
        objsList.extend(self._makeObjectList(IMobilePhone,
                                             _(u'Mobile Phones')))
        objsList.extend(self._makeObjectList(INet,
                                             _(u'Nets')))
        objsList.extend(self._makeObjectList(INotebook,
                                             _(u'Notebooks')))
        objsList.extend(self._makeObjectList(IOperatingSoftware,
                                             _(u'Operating Software')))
        objsList.extend(self._makeObjectList(IOutlet,
                                             _(u'Outlets')))
        objsList.extend(self._makeObjectList(IPatchPanel,
                                             _(u'Patch Panels')))
        objsList.extend(self._makeObjectList(IPatchPort,
                                             _(u'Patch Ports')))
        objsList.extend(self._makeObjectList(IPersonalComputer,
                                             _(u'Personal Computers')))
        objsList.extend(self._makeObjectList(IPhysicalLink,
                                             _(u'Physical Links')))
        objsList.extend(self._makeObjectList(IPrinter,
                                             _(u'Printers')))
        objsList.extend(self._makeObjectList(IRack,
                                             _(u'Racks')))
        objsList.extend(self._makeObjectList(IRoom,
                                             _(u'Rooms')))
        objsList.extend(self._makeObjectList(IService,
                                             _(u'Services')))
        objsList.extend(self._makeObjectList(ISnmpValue,
                                             _(u'Snmp Value')))
        objsList.extend(self._makeObjectList(ISwitch,
                                             _(u'Switches')))
        objsList.extend(self._makeObjectList(IX509Certificate,
                                             _(u'X509 Certificates')))
        objsList.append(getFirstLevelProductList(_(u'Products')))
#        objsList.extend(self._makeObjectList(IProduct,
#                                             'Products')))
        objsList.extend(self._makeObjectList(IAddress,
                                             _(u'Addresses')))
        objsList.extend(self._makeObjectList(IOrganization,
                                             _(u'Organizaions')))
        objsList.extend(self._makeObjectList(IPerson,
                                             _(u'Persons')))
        objsList.extend(self._makeObjectList(IContact,
                                             _(u'Contacts')))
        objsList.extend(self._makeObjectList(IContactItem,
                                             _(u'Contact items')))
        objsList.extend(self._makeObjectList(IWorkOrder,
                                             _(u'Work orders')))
        objsList.extend(self._makeObjectList(IPhysicalMedia,
                                             _(u'Physical media')))
        objsList.extend(self._makeObjectList(IRole,
                                             _(u'Roles')))
        objsList.extend(self._makeObjectList(IGroup,
                                             _(u'Groups')))
        #return self.reportPdfByQueryList(queryList)
        return self.reportPdfByObjectList(objsList, _(u'All objects'))

    def reportPersonsPdf(self):
        objsList = []
        objsList.extend(self._makeObjectList(IPerson,
                                             _(u'Persons')))
        return self.reportPdfByObjectList(objsList, _(u'All persons'))

    def appendFolder(self, folderClass):
        ApplicationSoftwareFolder.contentFactory
        ApplicationSoftwareFolder.shortName
        

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
