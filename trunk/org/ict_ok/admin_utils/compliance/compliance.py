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

# zope imports
from zope.app import zapi
from zope.interface import implements

# zc imports

# ict_ok.org imports
from org.ict_ok.admin_utils.reports.interfaces import IAdmUtilReports, IRptPdf
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.reports.rpt_document import RptDocument
from org.ict_ok.admin_utils.reports.rpt_title import RptTitle
from org.ict_ok.admin_utils.reports.rpt_para import RptPara
from org.ict_ok.admin_utils.compliance.interfaces import \
     IAdmUtilCompliance

logger = logging.getLogger("AdmUtilCompliance")


class AdmUtilCompliance(Supernode):
    """Compliance Utiltiy
    """
    implements(IAdmUtilCompliance)
    
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
        #document.setVolumeNo("1")
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
