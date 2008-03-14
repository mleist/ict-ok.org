# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0232,W0142,R0901
#
"""implementation of browser class of nagios-generator
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from zope.security import checkPermission
from zope.app.intid.interfaces import IIntIds

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IAdmUtilGeneratorNagios
from org.ict_ok.admin_utils.netscan.interfaces import INetScan

_ = MessageFactory('org.ict_ok')


class AdmUtilGeneratorNagiosDetails(SupernodeDetails):
    """
    Browser details for nagios-generator
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_editfields = SupernodeDetails.omit_editfields + []

    def actions(self):
        """
        gives us the action dict of the object
        """
        try:
            objId = getUtility(IIntIds).getId(self.context)
        except KeyError:
            objId = 1000
        retList = []
        if True:
        #if checkPermission('org.ict_ok.admin_utils.generators.nagios.View',
                           #self.context) and\
           #zapi.queryMultiAdapter((self.context, self.request),
                                  #name='shutdown.html') is not None:
            tmpDict = {}
            tmpDict['oid'] = u"c%sgenerate" % objId
            tmpDict['title'] = _(u"generate")
            tmpDict['href'] = u"%s/generate.html" % \
                   zapi.getPath(self.context)
            tmpDict['tooltip'] = _(u"generate nagios cfg")
            retList.append(tmpDict)
        return retList
    
    def generate(self):
        """
        starts all configured scanners for this net
        """
        #import pdb; pdb.set_trace()
        print "AdmUtilGeneratorNagiosDetails.generate start"
        print self.getConfig()
        print "AdmUtilGeneratorNagiosDetails.generate stop"
        #objNetScanner = getUtility(INetScan)
        #if objNetScanner is not None:
            #scannerList = objNetScanner.getScannerObjs()
            #for (name, obj) in scannerList:
                #obj.startScan(self.context)
        return self.request.response.redirect('./details.html')

    def getConfig(self):
        """Trigger configuration by web browser
        """
        return self.context.getConfig()


# --------------- forms ------------------------------------


class ViewAdmUtilGeneratorNagiosForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of graphviz adapter')
    fields = field.Fields(IAdmUtilGeneratorNagios).omit(\
        *AdmUtilGeneratorNagiosDetails.omit_viewfields)


class EditAdmUtilGeneratorNagiosForm(EditForm):
    """ Edit for for net """
    label = _(u'edit graphviz adapter')
    fields = field.Fields(IAdmUtilGeneratorNagios).omit(\
        *AdmUtilGeneratorNagiosDetails.omit_editfields)
