# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
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

# python imports
import logging
from datetime import datetime
from pytz import timezone

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.component import adapts

# ict_ok.org imports
from org.ict_ok.components.interface.interfaces import IInterface
from org.ict_ok.components.pc.interfaces import IPersonalComputer
from org.ict_ok.components.supernode.adapter.nagios import \
     GenNagios as ParentGenNagios
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios, IAdmUtilGeneratorNagios
from org.ict_ok.version import getIkVersion

logger = logging.getLogger("GenNagios")


class GenNagios(ParentGenNagios):
    """adapter implementation of Host -> nagios
    """

    implements(IGenNagios)
    adapts(IPersonalComputer)
    
    # modification of this attributes will trigger an new generation of
    # the config file
    attrList = ['objectID', 'hostname', 'ikName', 'genNagios']
    
    def __init__(self, context):
        ParentGenNagios.__init__(self, context)

    def fileOpen(self):
        """will open a filehandle to the specific object
        """
        objId = self.context.getObjectId()
        utilNagios = zapi.getUtility(IAdmUtilGeneratorNagios,
                                     name='AdmUtilGeneratorNagios')
        self.fileName = utilNagios.pathConfigData + u'/Hosts/%s.cfg' % objId
        ParentGenNagios.fileOpen(self)
        
    def wantsCheck(self):
        """object is configured to be checked?
        """
        return self.context.genNagios

    def traverse4nagiosGeneratorPre(self, level=0, comments=True):
        """graphviz configuration preamble
        """
        valueChanged = False
        if comments:
            self.write(u"%s## Pre (%s,%d) - PersonalComputerGenNagios" % \
                       ("\t" * level, self.context.ikName, level))
        if self.wantsCheck():
            valueChanged = True
            self.write(u"define host {\n")
            self.write(u"    use generic-host\n")
            self.write(u"    host_name %s\n" % (self.context.objectID))
            #self.write(u"    host_name %s\n" % (self.context.ikName))
            self.write(u"    display_name %s\n" % (self.context.ikName))
            self.write(u"    notes %s\n" % (self.context.objectID))
            #self.write(u"    alias %s\n" % self.context.hostname)
        else:
            self.write(u"# disabled by user\n")
        return valueChanged

    def traverse4nagiosGeneratorPost(self, level=0, comments=True):
        """graphviz configurations text after object
        """
        valueChanged = False
        if comments:
            self.write(u"%s## Post (%s,%d) - PersonalComputerGenNagios" % \
                       ("\t" * level, self.context.ikName, level))
        if self.wantsCheck():
            valueChanged = True
            self.write(u"    check_command check-host-alive\n")
            self.write(u"    max_check_attempts 3\n")
            self.write(u"    contact_groups admins\n")
            self.write(u"    notification_interval 0\n")
            self.write(u"    notification_period 24x7\n")
            self.write(u"    notification_options d,u,r\n")
            self.write(u"}\n\n")
        return valueChanged

    def traverse4nagiosGeneratorBody(self, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        valueChanged = False
        #if self.wantsCheck(from org.ict_ok.version import getIkVersion):
        if self.wantsCheck():
            if ParentGenNagios.traverse4nagiosGeneratorBody(self,
                                                         level,
                                                         comments):
                valueChanged = True
        return valueChanged

    def nagiosConfigFileOut(self, forceOutput=False, event=None):
        """Nagios-Filegenerator
        
        will produce the nagios configuration files
        
        forceOutput: False will check for a relevant attribute change
        True will alway generate a new config file
        
        event: None or the zope event from lifecycle
        """
        valueChanged = False
        ipv4 = None
        ipAddressList = []
        for interface in self.context.interfaces:
            for ipAddress in interface.ipAddresses:
                ipAddressList.append(ipAddress)
#        for if_name, if_obj in self.context.items():
#            if IInterface.providedBy(if_obj) and \
#               if_obj.ipv4List is not None and \
#               len (if_obj.ipv4List) > 0:
#                ipv4 = if_obj.ipv4List[0]
        if len(ipAddressList) > 0:
            if ParentGenNagios.nagiosConfigFileOut(self,
                                                   forceOutput,
                                                   event):
                valueChanged = True
        return valueChanged

    def nagiosConfigFileRemove(self):
        """remove old nagios configuration file for this object
        """
        #print "HostGenNagios.nagiosConfigFileRemove [%s]  -----------------------" % self.context.ikName
        ihostn = self.context.getObjectId() # internal object id as filename
        import os
        filename = u'/opt/nagios/etc/ict_ok/Hosts/'+ ihostn +'.cfg'
        try:
            os.remove(filename)
        except OSError, errtext:
            raise Exception, "No such configfile: '%s'" % filename
        return True # real values changed

def _test():
    import doctest
    options = doctest.ELLIPSIS
    return doctest.testfile('../../../doctests/nagios-host.txt', optionflags=options)

if __name__=="__main__":
    _test()
