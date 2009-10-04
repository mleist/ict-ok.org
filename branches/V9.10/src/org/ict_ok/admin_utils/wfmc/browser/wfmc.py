# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142,R0901
#
"""implementation of browser class of the wfmc-utility 
"""

__version__ = "$Id$"

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory
from zope.proxy import removeAllProxies

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.wfmc.wfmc import AdmUtilWFMC
#from org.ict_ok.admin_utils.wfmc.wfmc import AdmUtilWFMC
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubWfList(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Workflows')
    viewURL = 'wflist.html'
    weight = 90


# --------------- object details ---------------------------


class AdmUtilWFMCDetails(SupernodeDetails):
    """Browser implementation of WFMC picture generator
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    def getIMGFile(self):
        """get dot file and convert to png
        """
        imgtype = self.request.get('type', default='png')
        pdId = self.request.get('pdid', default=None)
        mode = self.request.get('mode', default=None)
        if mode and mode.lower() == "fview":
            self.request.response.setHeader('content-type',
                                            'image/%s' % imgtype)
            self.request.response.setHeader('content-disposition',
                                            'attachment; filename=\"%s.%s\"'\
                                            % (pdId,imgtype))
        if pdId:
            return self.context.getIMGFile(imgtype, pdId, mode)
        return None

    def getCmapxText(self):
        """get dot file and convert to client side image map
        """
        return self.context.getCmapxText(zapi.getRoot(self))

    def getValuePngHref(self):
        """get path of object as string
        """
        obj = removeAllProxies(self.context)
        return zapi.absoluteURL(obj, self.request)

    def getAllWfmcPDs(self):
        """get all registered Processdefinitions 
        """
        return AdmUtilWFMC.wf_pd_dict


# --------------- forms ------------------------------------




class AdmUtilWFMCWfList(AdmUtilWFMCDetails):
    label = _(u'Workflow List')

class AdmUtilWFMCWfView(AdmUtilWFMCDetails):
    label = _(u'Workflow View')

class ViewAdmUtilWFMCForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of workflow manager')
    factory = AdmUtilWFMC
    omitFields = AdmUtilWFMCDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class EditAdmUtilWFMCForm(EditForm):
    """ Edit for for net """
    label = _(u'edit workflow manager')
    factory = AdmUtilWFMC
    omitFields = AdmUtilWFMCDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
