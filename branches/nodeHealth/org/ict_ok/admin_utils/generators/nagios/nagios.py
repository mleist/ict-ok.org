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
"""Configuration adapter for nagios-config files
"""

__version__ = "$Id$"

# phython imports
import logging
from datetime import datetime
from pytz import timezone

# zope imports
from zope.app import zapi
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.version import getIkVersion
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IAdmUtilGeneratorNagios, IGenNagios
from org.ict_ok.admin_utils.generators.generators import \
     AdmUtilGenerators

logger = logging.getLogger("AdmUtilGeneratorNagios")
berlinTZ = timezone('Europe/Berlin')


class AdmUtilGeneratorNagios(AdmUtilGenerators):
    """Implementation of nagios configuration generator
    """
    implements(IAdmUtilGeneratorNagios)

    def __init__(self):
        AdmUtilGenerators.__init__(self)
        self.ikRevision = __version__

    def getConfig(self):
        """make configuration file
        TODO filename or filehandle must be an argument
        """
        dtHostCfg = datetime.now(berlinTZ)
        #fpHostCfg = open(u'/opt/ikomtrol/etc/Host.cfg', 'w+')
        fpHostCfg = open(u'/opt/nagios/etc/ict_ok/Host.cfg', 'w+')
        fpHostCfg.write(u"# Host.cfg\n")
        fpHostCfg.write(u"# generated by ict-ok.org Ver. %s (%s)\n\n" %
                        (getIkVersion(), dtHostCfg))

        dtHostGroupCfg = datetime.now(berlinTZ)
        #fpHostGroupCfg = open(u'/opt/ikomtrol/etc/HostGroup.cfg', 'w+')
        fpHostGroupCfg = open(u'/opt/nagios/etc/ict_ok/HostGroup.cfg', 'w+')
        fpHostGroupCfg.write(u"# HostGroup.cfg\n")
        fpHostGroupCfg.write(u"# generated by ict-ok.org Ver. %s (%s)\n\n" %
                             (getIkVersion(), dtHostGroupCfg))
        fpHostGroupCfg.write(u"define hostgroup {\n")
        fpHostGroupCfg.write(u"    hostgroup_name IKOMtrol\n")
        fpHostGroupCfg.write(u"    alias IKOMtrol-Systeme\n")
        fpHostGroupCfg.write(u"    members ")


        dtServiceCfg = datetime.now(berlinTZ)
        #fpServiceCfg = open(u'/opt/ikomtrol/etc/Service.cfg', 'w+')
        fpServiceCfg = open(u'/opt/nagios/etc/ict_ok/Service.cfg', 'w+')
        fpServiceCfg.write(u"# Service.cfg\n")
        fpServiceCfg.write(u"# generated by ict-ok.org Ver. %s (%s)\n\n" %
                           (getIkVersion(), dtServiceCfg))
        
        fileDict = {'HostCfg': fpHostCfg,
                    'HostGroupCfg': fpHostGroupCfg,
                    'ServiceCfg': fpServiceCfg}
        #cfgFile = open('/tmp/cfgNagiosFile', 'w')
        #import pdb; pdb.set_trace()
        its = zapi.getRoot(self).items()
        for (dummy_name, oobj) in its:
            if ISupernode.providedBy(oobj):
                try:
                    adapterGenNagios = IGenNagios(oobj)
                    if adapterGenNagios:
                        adapterGenNagios.traverse4nagiosGenerator(fileDict,
                                                                  level=1, 
                                                                  comments=False)
                except TypeError, errText:
                    logger.error(u"Problem in adaption of nagios config: %s" %\
                                 (errText))
                    
        fpHostGroupCfg.write(u"\n")
        fpHostGroupCfg.write(u"}\n\n")
        fpServiceCfg.write(u"# ok, generated in %s\n" %
                           (datetime.now(berlinTZ) - dtServiceCfg))
        fpServiceCfg.close()
        fpHostGroupCfg.write(u"# ok, generated in %s\n" %
                             (datetime.now(berlinTZ) - dtHostGroupCfg))
        fpHostGroupCfg.close()
        fpHostCfg.write(u"# ok, generated in %s\n" %
                        (datetime.now(berlinTZ) - dtHostCfg))
        fpHostCfg.close()
        return "aaa"
