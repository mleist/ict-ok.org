# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
#
"""Adapter implementation for generating graphviz-dot configuration
"""

__version__ = "$Id$"

# phython imports
import logging

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.service.interfaces import IService
from org.ict_ok.admin_utils.generators.nagios.adapter.supernode import \
     SupernodeGenNagios
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios

logger = logging.getLogger("ServiceGenNagios")


class ServiceGenNagios(SupernodeGenNagios):
    """adapter implementation of Service -> nagios
    """

    implements(IGenNagios)
    adapts(IService)
    
    def __init__(self, context):
        print "ServiceGenNagios.__init__"
        SupernodeGenNagios.__init__( self, context)

    def traverse4nagiosGeneratorPre(self, fileDict, level=0, comments=True):
        """graphviz configuration preamble
        """
        tmp_interface = zapi.getParent(self.context)
        tmp_host = zapi.getParent(tmp_interface)
        if comments:
            print >> fileDict['ServiceCfg'], \
                  "%s## Pre (%s,%d) - ServiceGenNagios" % \
                  ("\t" * level, self.context.ikName, level)
        fileDict['ServiceCfg'].write( "define service {\n")
        fileDict['ServiceCfg'].write( "    use generic-ping\n")
        #fileDict['ServiceCfg'].write( "    host_name %s\n" % \
        #realHost.hostname)
        fileDict['ServiceCfg'].write( "    host_name %s\n" % tmp_host.objectID)
        #fileDict['ServiceCfg'].write( "    hostgroup_name ict_ok\n")
        #fileDict['ServiceCfg'].write( "    service_description %s-%s\n" % \
        #(realHost.ip, realService.description))
        ##if len(self.context.ikDesc) > 0:
            ##fileDict['ServiceCfg'].write( "    service_description %s\n" % \
                                          ##(self.context.ikDesc))
        ##else:
            ##fileDict['ServiceCfg'].write( "    service_description %s\n" % \
                                          ##(self.context.ikName))
        fileDict['ServiceCfg'].write( "    service_description %s\n" % \
                                      (self.context.getDcTitle()))
        fileDict['ServiceCfg'].write( "    contact_groups    admins\n")
        fileDict['ServiceCfg'].write( "    check_period    24x7\n")
        fileDict['ServiceCfg'].write( "    notification_interval    0\n")
        fileDict['ServiceCfg'].write( "    notification_options    w,u,c,r\n")
        fileDict['ServiceCfg'].write( "    notification_period    24x7\n")
        fileDict['ServiceCfg'].write( "    check_command    check_ssh!1!22\n")
        fileDict['ServiceCfg'].write( "    max_check_attempts    3\n")
        fileDict['ServiceCfg'].write( "    normal_check_interval    5\n")
        fileDict['ServiceCfg'].write( "    retry_check_interval    1\n")
        fileDict['ServiceCfg'].write( "}\n\n")


    def traverse4nagiosGeneratorPost(self, fileDict, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            print >> fileDict['ServiceCfg'], \
                  "%s## Post (%s,%d) - ServiceGenNagios" % \
                  ("\t" * level, self.context.ikName, level)

    #def traverse4nagiosGeneratorPre(self, fileDict, level=0, comments=True):
        #"""graphviz configuration preamble
        #"""
        #if comments:
            #print >> fileDict['HostCfg'], \
                  #"%s## Pre (%s,%d) - HostGenNagios" % \
                  #("\t" * level, self.context.ikName, level)
        #fileDict['HostCfg'].write(u"define host {\n")
        #fileDict['HostCfg'].write(u"    use generic-host\n")
        #fileDict['HostCfg'].write(u"    host_name %s\n" % \
        #(self.context.objectID))
        #fileDict['HostCfg'].write(u"    alias %s\n" % self.context.hostname)
        ##fileDict['HostCfg'].write("    address %s\n" % realObj.ip)
        #fileDict['HostGroupCfg'].write(u"%s," % self.context.objectID)
        


    #def traverse4nagiosGeneratorPost(self, fileDict, level=0, comments=True):
        #"""graphviz configurations text after object
        #"""
        #if comments:
            #print >> fileDict['HostCfg'], \
                  #"%s## Post (%s,%d) - HostGenNagios" % \
                  #("\t" * level, self.context.ikName, level)
        #fileDict['HostCfg'].write(u"    check_command check-host-alive\n")
        #fileDict['HostCfg'].write(u"    max_check_attempts 3\n")
        #fileDict['HostCfg'].write(u"    contact_groups Admins\n")
        #fileDict['HostCfg'].write(u"    notification_interval 0\n")
        #fileDict['HostCfg'].write(u"    notification_period 24x7\n")
        #fileDict['HostCfg'].write(u"    notification_options d,u,r\n")
        #fileDict['HostCfg'].write(u"}\n\n")
    #def genServiceConfig( self, proxyObj, fileH):
        #"""
        #erzeugt die Konfigurationsdatei
        #"""
        #realService = removeAllProxies( proxyObj)
        #realHost = zapi.getParent( realService)
        #fileH.write( "define service {\n")
        #fileH.write( "    use generic-ping\n")
        ##fileH.write( "    host_name %s\n" % realHost.hostname)
        #fileH.write( "    host_name %s\n " % zapi.getPath(realHost))
        ##fileH.write( "    hostgroup_name ict_ok\n")
        ##fileH.write( "    service_description %s-%s\n" % \
        ##(realHost.ip, realService.description))
        #fileH.write( "    service_description %s\n" % (realService.description))
        #fileH.write( "    contact_groups    Admins\n")
        #fileH.write( "    check_period    24x7\n")
        #fileH.write( "    notification_interval    0\n")
        #fileH.write( "    notification_options    w,u,c,r\n")
        #fileH.write( "    notification_period    24x7\n")

        ##print "ddd: name:%s port:%s porttype:%s" % (realService.description,
                                                    ##realService.port, 
                                                    ##type(realService.port))
        #if str(realService.port) == u"80":     ## http
            #try:
                #fileH.write( "    check_command    check_httpauth!%s!%s\n" % \
                #(realService.authname.replace(" ", "\ "),
                 #realService.authpasswd.replace(" ", "\ ")))
            #except:
                #fileH.write( "    check_command    check_http\n")
        #elif str(realService.port) == u"22":   ## ssh
            #fileH.write( "    check_command    check_ssh!1!22\n")
        #elif str(realService.port) == u"53":   ## domain
            #fileH.write( "    check_command    check_dns\n")
        #elif str(realService.port) == u"25":   ## smtp
            #fileH.write( "    check_command    check_smtp\n")
        #elif str(realService.port) == u"23":   ## telnet
            #fileH.write( "    check_command    check_telnet\n")
        #elif str(realService.port) == u"67":   ## dhcp
            #fileH.write( "    check_command    check_dhcp\n")
        #elif str(realService.port) == u"143":   ## imap
            #fileH.write( "    check_command    check_imap\n")
        #elif str(realService.port) == u"389":   ## ldap
            #fileH.write( "    check_command    check_ldap!%s\n" % \
            #(realService.basedn.replace(" ", "\ ")))
        #elif str(realService.port) == u"443":   ## https
            #fileH.write( "    check_command    check_https\n")
            ##print "jepp"
        #elif str(realService.port) == u"3128":   ## squid
            #fileH.write( "    check_command    check_squid!3128!http://www.essen.de\n")
        #elif str(realService.port) == u"0":   ## squid
            #fileH.write( "    check_command    check_ping!100.0,20%!500.0,60%\n")
        #else:
            #fileH.write( "    check_command    check_ping!100.0,20%!500.0,60%\n")
        #fileH.write( "    max_check_attempts    3\n")
        #fileH.write( "    normal_check_interval    5\n")
        #fileH.write( "    retry_check_interval    1\n")
        #fileH.write( "}\n\n")
        #return None
