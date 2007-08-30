# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232
#
"""implementation of browser class of esx_vim handler
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.security import checkPermission
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
#from org.ict_ok.admin_utils.esx_vim.esx_vim import globalEsxVimUtility

_ = MessageFactory('org.ict_ok')

class AdmUtilEsxVimDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_editfields = SupernodeDetails.omit_editfields + []

    def getInstanceCounter(self):
        """convert instance counter for display
        """
        return self.context.getInstanceCounter()

    def getEsxVimTime(self):
        """convert esx_vim timestamp for display
        """
        return self.context.getEsxVimTime()

    #def getGlobalEsxVimUtility(self):
        #return globalEsxVimUtility


class EsxVimObjDetails(object):
    """ Class for Web-Browser-Details """
    displayName = u"Display: EsxVimObjDetails"
    def getDisplayName(self):
        """ return Type of display class """
        return self.displayName

class EsxVimDatacenterDetails(EsxVimObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: EsxVimDatacenterDetails"

class EsxVimDatastoreDetails(EsxVimObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: EsxVimDatastoreDetails"

class EsxVimNetworkDetails(EsxVimObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: EsxVimNetworkDetails"

class EsxVimFolderDetails(EsxVimObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: EsxVimFolderDetails"

class EsxVimVirtualMachineDetails(EsxVimObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: EsxVimVirtualMachineDetails"
    
    def actions(self):
        """
        gives us the action dict of the object
        """
        try:
            objId = getUtility(IIntIds).getId(self.context)
        except KeyError:
            objId = 1000
        retList = []
        if checkPermission('org.ict_ok.admin_utils.esx_vim.Admin',
                           self.context) and\
           zapi.queryMultiAdapter((self.context, self.request),
                                  name='shutdown.html') is not None:
            tmpDict = {}
            tmpDict['oid'] = u"c%s" % objId
            tmpDict['title'] = _(u"shutdown")
            tmpDict['href'] = u"%s/@@shutdown.html" % \
                   zapi.getPath(self.context)
            tmpDict['tooltip'] = _(u"shutdow the virtual machine")
            retList.append(tmpDict)
        return retList

class EsxVimHostSystemDetails(EsxVimObjDetails):
    """ Class for Web-Browser-Details """
    displayName = u"Display: EsxVimHostSystemDetails"
