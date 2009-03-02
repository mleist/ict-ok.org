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
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.security import checkPermission
from zope.app.rotterdam.xmlobject import setNoCacheHeaders

# zc imports

# ict-ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.version import getIkVersion
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     getUserTimezone
from org.ict_ok.components.supernode.browser.supernode import SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.reports.reports import AdmUtilReports


_ = MessageFactory('org.ict_ok')


# --------------- helper functions -------------------------

# --------------- menu entries -----------------------------

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
                   (zapi.getPath(self.context))
            tmpDict['tooltip'] = _(u"will generate a test pdf file")
            retList.append(tmpDict)
        if checkPermission('org.ict_ok.admin_utils.reports.generate.pdf',
                           self.context):
            tmpDict = {}
            tmpDict['oid'] = u"c%sgenerate_all_pdf" % objId
            tmpDict['title'] = _(u"generate all pdf")
            tmpDict['href'] = u"%s/@@generate_all_pdf" % \
                   (zapi.getPath(self.context))
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
