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
from lxml import etree

# zope imports
from zope.interface import implements
from zope.xmlpickle import toxml, fromxml, loads

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
        print "--->", etree.tostring(treeTemplate, pretty_print=True)
        
        #root.append(treet)

        its = self.items()
        for (dummy_name, oobj) in its:
            if ISuperclass.providedBy(oobj):
                rootTmp.append( oobj.asETree())
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
                    if len(req.categories) > 0:
                        obj_cat_set = set(obj.categories)
                        req_cat_set = set(req.categories)
                        if not obj_cat_set.isdisjoint(req_cat_set):
                            if req is not in obj.requirements:
                                obj.requirements.append(req)

    def delete_requirements(self):
        """ delete all Categories from Components
        """
        objList = objectsWithInterface(IComponent)
        for obj in objList:
            obj.requirements = []
