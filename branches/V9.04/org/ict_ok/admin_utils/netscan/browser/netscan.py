# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=E1101,E0611,W0232,W0142,R0901
#
"""implementation of browser class of Object-Message-Queue-Utility
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.netscan.interfaces import IScanner
from org.ict_ok.admin_utils.netscan.netscan import NetScan

_ = MessageFactory('org.ict_ok')


class NetScanDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    _zopeRuntimeInfoFields = (
        "ZopeVersion",
        "PythonVersion",
        "PythonPath",
        "SystemPlatform",
        "PreferredEncoding",
        "FileSystemEncoding",
        "CommandLine",
        "ProcessId"
        )
    _zopeRuntimeInfoUnavailable = _("Unavailable")
    
    def getAllScannerObjs(self):
        """
        get list of Scanner-Tupel (name, obj)
        """
        retList = []
        for name, scanner in self.context.getAllScannerObjs():
            retDict = {}
            retDict['name'] = name
            retDict['href'] = zapi.getPath(scanner) + '/@@status'
            retList.append(retDict)
        return retList
        
    def getScannerObjs(self):
        """
        get list of Scanner-Tupel (name, obj)
        """
        retList = []
        for name, scanner in self.context.getScannerObjs():
            retDict = {}
            retDict['name'] = name
            retDict['href'] = zapi.getPath(scanner) + '/@@status'
            retList.append(retDict)
        return retList
        
    def getAAA(self):
        """convert start counter for display
        """
        a = []
        #a = {}
        utilList = [util for name, util in zapi.getUtilitiesFor(IScanner)]
        #from zope.component import getSiteManager
        #a.append(dir(getSiteManager()))
        
        #print "ttttttt: [%s]" % ([(role, type(role)) for name, role in zapi.getUtilitiesFor(IScanner)] )
        #obj = zapi.getAllUtilitiesRegisteredFor(IScanner)
        #a['type'] = type(obj)
        #a['dir'] = dir(obj)
        #a['obj'] = obj
        #print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        for i in utilList:
            b = {}
            #b['getName'] = i.getName()
            #b['name'] = i.name
            #b['plist'] = [i.__name__ for i in providedBy(i)]
            #b['pd'] = dir(providedBy(i))
            b['__name__'] = i.__name__
            #print "++++++++++++++++++++++++++: %s" % (IScanner in providedBy(i).isImplementedBy()
            #b['prov'] = providedBy(i)
            #b['prov_i'] = providedBy(i).interfaces()
            #b['i_in_prov_i'] = IScanner in providedBy(i).interfaces()
            #b['dp'] = directlyProvidedBy(i)
            #b['ddp'] = dir(directlyProvidedBy(i))
            #b['dpi'] = list(directlyProvidedBy(i).interfaces())
            #b['type_prov'] = type(providedBy(i))
            #b['dir_prov'] = dir(providedBy(i))
            #b['impl'] = implementedBy(i)
            b['type'] = type(i)
            b['dir'] = dir(i)
            b['obj'] = i
            #for j in b['dp']:
            #    print "::%s::" % j
            a.append(b)
        return a 
    

# --------------- forms ------------------------------------


class DetailsNetScanForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of all net scanner')
    factory = NetScan
    omitFields = NetScanDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class EditNetScanForm(EditForm):
    """ Edit for for net """
    label = _(u'edit central net scanner')
    factory = NetScan
    omitFields = NetScanDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
