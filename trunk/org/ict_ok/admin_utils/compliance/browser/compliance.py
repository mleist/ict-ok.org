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
"""
"""implementation of browser class of eventCrossbar handler
"""

__version__ = "$Id$"

# python imports
import os
from datetime import datetime
import tempfile

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.dublincore.interfaces import IZopeDublinCore
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.security import checkPermission
from zope.app.rotterdam.xmlobject import setNoCacheHeaders

# zc imports
from zc.table.column import GetterColumn
from zc.table.table import StandaloneFullFormatter

# z3c imports
from z3c.form import field
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports
from org.ict_ok.version import getIkVersion
from org.ict_ok.admin_utils.usermanagement.usermanagement import \
     getUserTimezone
from org.ict_ok.admin_utils.compliance.interfaces import \
     IAdmUtilCompliance
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.admin_utils.compliance.interfaces import IRequirement

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


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
                   (zapi.getPath(self.context))
            tmpDict['tooltip'] = _(u"will generate a all pdf file")
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


# --------------- forms ------------------------------------


class DetailsAdmUtilComplianceForm(DisplayForm):
    """ Display form for the object """
    
    label = _(u'settings of Compliance')
    fields = field.Fields(IAdmUtilCompliance).omit(
       *AdmUtilComplianceDetails.omit_viewfields)

    def update(self):
        if False:
            from zope.component import adapts, queryUtility
            from schooltool.requirement.interfaces import IScoreSystem
            from zope.app.intid import IntIds
            from zope.app.intid.interfaces import IIntIds
            uu2 = queryUtility(IScoreSystem, "Comp_Pass/Fail")
            uu3 = queryUtility(IIntIds)
            from org.ict_ok.admin_utils.compliance.requirement import Requirement
            from zope.proxy import removeAllProxies
            obj = removeAllProxies(self.context)
            #a1 = Requirement("a1")
            #a2 = Requirement("a2")
            #a3 = Requirement("a3")
            #aa = Requirement("a")
            #aa['a1'] = a1
            #aa['a2'] = a2
            #aa['a3'] = a3
            managementOBJ = obj
            try:
                del managementOBJ['alle Requirements']
            except KeyError:
                pass
            try:
                del managementOBJ['IT-Sicherheitskonzept']
            except KeyError:
                pass
        DisplayForm.update(self)

def getTitel(item, formatter):
    """
    Titel for Overview
    """
    try:
        return item.ikName
    except TypeError:
        return str(item.__class__.__name__)

from org.ict_ok.components.superclass.browser.superclass import \
     Overview, getModifiedDate, raw_cell_formatter, \
     link, getActionBottons, getSize
class AdmUtilRequirementDisplay(Overview):
    """for 1st level Requirements
    """
    label = _(u'display requirements')
    columns = (
        GetterColumn(title=_('Title'),
                     getter=getTitel,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('Modified On'),
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
    sort_columns = [1]
    status = None
    
    def objs(self):
        """List of Content objects"""
        return [obj
                for obj in self.context.values()
                if IRequirement.providedBy(obj)]

class AdmUtilRequirementDisplayAll(AdmUtilRequirementDisplay):
    """for all Requirements
    """
    label = _(u'display all requirements (not yet)')

class EditAdmUtilComplianceForm(EditForm):
    """ Display form for the object """
    
    label = _(u'edit Compliance properties')
    fields = field.Fields(IAdmUtilCompliance).omit(
       *AdmUtilComplianceDetails.omit_editfields)
