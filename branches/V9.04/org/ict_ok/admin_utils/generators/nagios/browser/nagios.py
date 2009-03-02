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

# python imports

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from zope.security import checkPermission
from zope.app.intid.interfaces import IIntIds
from zope.app.pagetemplate.urlquote import URLQuote

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.generators.nagios.nagios import \
     AdmUtilGeneratorNagios

_ = MessageFactory('org.ict_ok')


class AdmUtilGeneratorNagiosDetails(SupernodeDetails):
    """
    Browser details for nagios-generator
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_editfields = SupernodeDetails.omit_editfields + \
                    ['lastConfigFileChange', 'lastDeamonReload']

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
            quoter = URLQuote(self.request.getURL())
            tmpDict = {}
            tmpDict['oid'] = u"c%sgenerate" % objId
            tmpDict['title'] = _(u"generate")
            tmpDict['href'] = u"%s/@@generate.html?nextURL=%s" % \
                   (zapi.getPath( self.context),
                    quoter.quote())
            tmpDict['tooltip'] = _(u"generate nagios cfg")
            retList.append(tmpDict)
        return retList
    
    def generate(self):
        """
        starts all configured scanners for this net
        """
        print "AdmUtilGeneratorNagiosDetails.generate start"
        print self.allConfigFilesOut()
        print "AdmUtilGeneratorNagiosDetails.generate stop"
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def allConfigFilesOut(self):
        """Trigger configuration by web browser
        """
        return self.context.allConfigFilesOut()


# --------------- forms ------------------------------------


class DetailsAdmUtilGeneratorNagiosForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of nagios generator')
    factory = AdmUtilGeneratorNagios
    omitFields = AdmUtilGeneratorNagiosDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class EditAdmUtilGeneratorNagiosForm(EditForm):
    """ Edit for for net """
    label = _(u'edit graphviz adapter')
    factory = AdmUtilGeneratorNagios
    omitFields = AdmUtilGeneratorNagiosDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
