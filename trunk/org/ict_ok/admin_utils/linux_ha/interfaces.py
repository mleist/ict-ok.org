# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232,W0622
#
"""Interface of LinuxHa-Utility

This utility is an interface to the virtual infrastructure
management of an esx-serverfarm (VmWare (tm))

base of this interface is located in:
  "VMware Infrastructure Perl Toolkit"
  http://sourceforge.net/projects/viperltoolkit/

  The VMware Virtual Infrastructure Perl Toolkit (VI Perl Toolkit)
  provides a set of libraries and scripts to manage and control
  VMware virtual machines and servers using the VMware
  Virtual Infrastructure Web Service interface.

this perl-library is wrapped by PyPerl:
http://wiki.python.org/moin/PyPerl
http://www.felix-schwarz.name/files/opensource/pyperl/
    -> pyperl-dist-1.0.1c.tar.gz

"""

__version__ = "$Id$"

# zope imports
from zope.interface import Attribute, Interface
from zope.schema import Bool, Int, Password, TextLine
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.schema.ipvalid import HostIpValid
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')

class IAdmUtilLinuxHa(ISupernode):
    """
    major component for registration and event distribution 
    """
    LinuxHaServerActive = Bool(
        title = _("HA-Cluster active"),
        description = _("HA-Cluster connector active"),
        default = False,
        required = False)

    LinuxHaServerIp = HostIpValid(
        min_length = 1,
        max_length = 30,
        title = _("HA-Cluster IP"),
        description = _("Active IP address of the ha cluster"),
        default = u"0.0.0.0",
        required = False)
    
    LinuxHaServerPort = Int(
        min = 1,
        max = 65535,
        title = _("HA-Cluster Port"),
        description = _("Port of of the ha cluster"),
        default = 5560,
        required = False)
    
    LinuxHaUsername = TextLine(
        title = _("HA-Cluster Username"),
        description = _("Name of user with admin rights on ha cluster"),
        default = u"username",
        required = False)

    LinuxHaPassword = Password(
        title = _("HA-Cluster Password"),
        description = _("Password of user with admin rights on ha cluster"),
        default = u"password",
        required = False)

    connState = Attribute("Connection State")

    def keys(self):
        '''See interface `IReadContainer`'''

    def __iter__(self):
        '''See interface `IReadContainer`'''

    def __getitem__(self, key):
        '''See interface `IReadContainer`'''

    def get(self, key, default=None):
        '''See interface `IReadContainer`'''

    def values(self):
        '''See interface `IReadContainer`'''

    def __len__(self):
        '''See interface `IReadContainer`'''

    def items(self):
        '''See interface `IReadContainer`'''

    def __contains__(self, key):
        '''See interface `IReadContainer`'''

    def connect2HaCluster(self):
        ''' '''


class IGlobalLinuxHaUtility(Interface):
    """
    IGlobalLinuxHaUtility
    """
    lastLinuxHa = TextLine(
        min_length = 5,
        max_length = 40,
        title = _("Last LinuxHa Contact"),
        description = _("Date of last VmWare-Esx Vim contact"),
        default = _("00.00.0000"),
        required = True)
    
    def getUtilityVersion(self):
        """ global und svn Version of Utility """
        
    def getUptime(self):
        """uptime of Utility"""
