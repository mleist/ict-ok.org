# -*- coding: utf-8 -*-
#
# Copyright (c) 2007, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
"""Interface of compliance utility

the compliance utility should store the compliance/requirement-templates
for the host- or service-instances
"""

__version__ = "$Id$"

# python imports
import os
import logging
import pickle
from datetime import datetime
from lxml import etree

# zope imports
from zope.interface import implements
from zope.xmlpickle import toxml, fromxml, loads
from zope.app import zapi
from zope.app.catalog.interfaces import ICatalog
from zope.component import getUtility

# zc imports

# ict_ok.org imports
from org.ict_ok.admin_utils.reports.interfaces import IRptPdf
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.admin_utils.reports.rpt_document import RptDocument
from org.ict_ok.admin_utils.compliance.interfaces import \
     IAdmUtilCompliance, IImportXmlData
from org.ict_ok.components.superclass.superclass import objectsWithInterface
from org.ict_ok.admin_utils.compliance.interfaces import IRequirement
from org.ict_ok.admin_utils.compliance.requirement import Requirement
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.admin_utils.categories.interfaces import IAdmUtilCategories

logger = logging.getLogger("AdmUtilCompliance")


class AdmUtilCompliance(Supernode):
    """Compliance Utiltiy
    """
    implements(IAdmUtilCompliance,
               IImportXmlData)
    
    def append(self, subObj):
        """ append Requirement
        """
        if hasattr(subObj, 'objectID'):
            self[subObj.objectID] = subObj
        else:
            self[subObj.ikName] = subObj

    def generateAllPdf(self, absFilename, authorStr, versionStr):
        """
        will generate a complete pdf report
        """
        files2delete = []
        document = RptDocument(absFilename)
        document.setAuthorName(authorStr)
        document.setVersionStr(versionStr)
        its = self.items()
        for (dummy_name, oobj) in its:
            if ISuperclass.providedBy(oobj):
                try:
                    adapterRptPdf = IRptPdf(oobj)
                    if adapterRptPdf:
                        adapterRptPdf.document = document
                        adapterRptPdf.traverse4Rpt(1, False)
                        files2delete.extend(adapterRptPdf.files2delete)
                        del adapterRptPdf
                except TypeError, errText:
                    logger.error(u"Problem in adaption of pdf report: %s" %\
                                 (errText))
        document.buildPdf()
        for i_filename in files2delete:
            try:
                os.remove(i_filename)
            except OSError:
                pass

    def exportXmlData(self):
        """get data file for all objects"""
        #dataStructure = {
            #'objects': ['a', 'b', 'c'],
            #'conns': [1, 2, 3],
            #}
        dataStructure = {
            'objects': [],
            }
        its = self.items()
        for (dummy_name, oobj) in its:
            if ISuperclass.providedBy(oobj):
                dataStructure['objects'].append(oobj.ikName)
#        sitemanger = zapi.getParent(self)
#        locSitemanager = zapi.getParent(sitemanger)
#        root_folder = zapi.getParent(locSitemanager)
#        for folder in root_folder.values():
#            for obj in folder.values():
#                obj.getAllExportData(dataStructure)
        python_pickle = pickle.dumps(dataStructure)
        return toxml(python_pickle)

    def importReqSet(self, xmlElement, importOnNode=None):
        """import Requirement from xml data
        """
        print "importReqSet(%s)" % xmlElement
        print "tags: %s, text: %s" % (xmlElement.tag, xmlElement.text)
        utilCategories = getUtility(IAdmUtilCategories,
                                    name='AdmUtilCategories')
        reqTitle = xmlElement.find('Title')
        reqTitleText = None
        if reqTitle is not None:
            reqTitleText = unicode(reqTitle.text)
        reqCategoriesList = xmlElement.findall('Categories/*')
        attrib={}
        oldReqObject = None
        str_objectID = xmlElement.get('uid')
        if str_objectID is not None:
            attrib['objectID'] = unicode(str_objectID)
            my_catalog = zapi.getUtility(ICatalog)
            res = my_catalog.searchResults(oid_index=attrib['objectID'])
            if len(res) > 0:
                oldReqObject = iter(res).next()
                print "oldReqObject: ", oldReqObject
        str_ikAuthor = xmlElement.get('author')
        if str_ikAuthor is not None:
            attrib['ikAuthor'] = unicode(str_ikAuthor)
        str_copyright = xmlElement.get('copyright')
        if str_copyright is not None:
            attrib['copyright'] = unicode(str_copyright)
        str_version = xmlElement.get('version')
        if str_version is not None:
            attrib['version'] = unicode(str_version)
        str_validAsFirst = xmlElement.get('validAsFirst')
        if str_validAsFirst is not None:
            attrib['validAsFirst'] = bool(str_validAsFirst)
        str_resubmitDate = xmlElement.get('resubmitDate')
        if str_resubmitDate is not None:
            attrib['resubmitDate'] = \
                datetime.strptime(str_resubmitDate,
                                  '%Y-%m-%d %H:%M:%S')
        attrib['categories'] = []
        if reqCategoriesList is not None:
            internalCategoriesDict = utilCategories.getNamedReqDict()
            for reqCategoryElement in reqCategoriesList:
                tmpCategoryName = reqCategoryElement.text
                if internalCategoriesDict.has_key(tmpCategoryName):
                    categoryObj = internalCategoriesDict[tmpCategoryName]
                    attrib['categories'].append(categoryObj)
        if oldReqObject is not None:
            if reqTitleText is not None and \
                not reqTitleText == oldReqObject.ikName:
                    print "change1: ", (oldReqObject.ikName, reqTitleText)
                    oldReqObject.ikName = reqTitleText
                    IBrwsOverview(oldReqObject).setTitle(reqTitleText)
            attrObjectID = attrib.pop('objectID')
            for (name, value) in attrib.items():
                if not getattr(oldReqObject, name) == value:
                    print "change2: ", (oldReqObject, name, value)
                    setattr(oldReqObject, name, value)
        else:
            obj = Requirement(reqTitleText, **attrib)
            IBrwsOverview(obj).setTitle(reqTitleText)
            obj.__post_init__()
            importOnNode[obj.objectID] = obj
            obj.store_refs(**attrib)
            oldReqObject = obj
        children = xmlElement.findall('Req')
        for child in children:
            self.importReqSet(child, importOnNode=oldReqObject)

    def importReqXmlData(self, xmlTree):
        """set data for all objects from xml-tree"""
#        import pdb
#        pdb.set_trace()
        reqList = xmlTree.getroot().findall('Req')
        for reqElement in reqList:
            self.importReqSet(reqElement, importOnNode=self)

    def appendReqXmlData(self, objects, rootElement):
        for (dummy_name, oobj) in objects:
            if ISuperclass.providedBy(oobj):
                rootElement.append(oobj.asETree())

    def exportReqXmlData(self):
        # ...
        import StringIO
        rootTmp = etree.Element("Req")
        xmlTemplate = """<?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE root SYSTEM "test" []><Req></Req>"""
        xmlTemplate = """<?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE Req PUBLIC "-//IKOMtrol//DTD Reqs 1.0//EN" "reqs.dtd" []>
        <Req>
        <a></a>
        </Req>
        """
        treeTemplate = etree.parse(StringIO.StringIO(xmlTemplate))

#        xml = et.XML("<root><test/><a>whatever</a><end_test/></root>")
#        root = tree.getroot()
#        root[:] = xml
#        root.text, root.tail = xml.text, xml.tail
#        print et.tostring(tree, xml_declaration=True, encoding="utf-8")
        
        
        
        #root.append(etree.Element('!DOCTYPE Req PUBLIC "-//IKOMtrol//DTD Reqs 1.0//EN" "reqs.dtd" []'))
        #treet = etree.fromstring('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html></html>')
        #print "--->", etree.tostring(treeTemplate, pretty_print=True)
        
        #root.append(treet)

        its = self.items()
        self.appendReqXmlData(its, rootTmp)
#        for (dummy_name, oobj) in its:
#            if ISuperclass.providedBy(oobj):
#                rootTmp.append( oobj.asETree())
        #etree.tostring(etree.ElementTree(tree.getroot()))
        #import pdb
        #pdb.set_trace()
        
        xml = etree.XML("<root><test/><a>whatever</a><end_test/></root>")
        rootTemplate = treeTemplate.getroot()
        rootTemplate[:] = xml
        rootTemplate.text, rootTemplate.tail = xml.text, xml.tail
        
        
        #et = etree.ElementTree(root)
        # <!DOCTYPE Req PUBLIC "-//IKOMtrol//DTD Reqs 1.0//EN" "reqs.dtd" []>
#        et.docinfo.doctype = u'1'
#        et.docinfo.encoding = u'2'
#        et.docinfo.externalDTD = u'3'
#        et.docinfo.internalDTD = u'4'
#        et.docinfo.root_name = u'5'
#        et.docinfo.standalone = u'6'
#        et.docinfo.system_url = u'7'
#        et.docinfo.xml_version = u'8'
        s = """<?xml version="1.0" encoding="utf-8"?>
        <!DOCTYPE root SYSTEM "test" []>
        <root>
        <a></a>
        </root>
        """
        newTree = etree.parse(StringIO.StringIO(xmlTemplate))
        
        xml = etree.XML("<root><test/><a>whatever</a><end_test/></root>")
        newRoot = newTree.getroot()
        newRoot[:] = rootTmp
        newRoot.text, newRoot.tail = rootTmp.text, rootTmp.tail
        titleObj = etree.Element("Title")
        titleObj.text = u'Root'
        newRoot.insert(0, titleObj)
        #return etree.tostring(newTree, xml_declaration=True, encoding="utf-8")
        return etree.tostring(newTree, pretty_print=True, xml_declaration=True, encoding="utf-8")

    def match_requirements(self):
        """ match all Components with Categories on all Requirements with
        same Categories
        """
        objList = objectsWithInterface(IComponent)
        reqList = objectsWithInterface(IRequirement)
        for obj in objList:
            if len(obj.categories) > 0:
                for req in reqList:
                    if req.validAsFirst and len(req.categories) > 0:
                        obj_cat_set = set(obj.categories)
                        req_cat_set = set(req.categories)
                        if not obj_cat_set.isdisjoint(req_cat_set):
                            if not req in obj.requirements:
                                obj.requirements.append(req)
                                obj._p_changed = 1

    def delete_requirements(self):
        """ delete all Categories from Components
        """
        objList = objectsWithInterface(IComponent)
        for obj in objList:
            obj.requirements = []
