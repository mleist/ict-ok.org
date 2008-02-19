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
"""Interface of EsxVim-Utility

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

class IAaa(Interface):
    """
    major component for registration and event distribution 
    """
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


class IAdmUtilEsxVim(ISupernode):
    """
    major component for registration and event distribution 
    """
    esxVimServerActive = Bool(
        title = _("ESX VIM active"),
        description = _("Esx connector active"),
        default = False,
        required = False)

    esxVimServerIp = HostIpValid(
        min_length = 1,
        max_length = 30,
        title = _("ESX VIM IP"),
        description = _("Active IP address of esx vim-server"),
        default = u"0.0.0.0",
        required = False)
    
    esxVimServerPort = Int(
        min = 1,
        max = 65535,
        title = _("ESX VIM Port"),
        description = _("Port of esx vim-server"),
        default = 443,
        required = False)
    
    esxVimUsername = TextLine(
        title = _("ESX VIM Username"),
        description = _("Name of user with admin rights on esx vim-server"),
        default = u"username",
        required = False)

    esxVimPassword = Password(
        title = _("ESX VIM Password"),
        description = _("Password of user with admin rights on esx vim-server"),
        default = u"password",
        required = False)
    
    connStatus = Attribute("Connection State")
    apiFullName = Attribute("Fullname of ESX VIM Api")

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


class IAdmUtilEsxVim2(Interface):
    """
    major component for registration and event distribution 
    """
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


class IGlobalEsxVimUtility(Interface):
    """
    IGlobalEsxVimUtility
    """
    lastEsxVim = TextLine(
        min_length = 5,
        max_length = 40,
        title = _("Last EsxVim Contact"),
        description = _("Date of last VmWare-Esx Vim contact"),
        default = _("00.00.0000"),
        required = True)
    
    def getUtilityVersion(self):
        """ global und svn Version of Utility """
        
    def getUptime(self):
        """uptime of Utility"""


class IEsxVimObj(Interface):
    """ Base class for the esx vim objects """
    name = Attribute("esx object name")
    overallStatus = Attribute("esx object state")
    def eval_on_obj(self, eval_text='name()', fnct_args=None):
        """ evaluate an text with optional arguments on this object """
    def esxtime2python(self, time):
        """ convert time string from esx to python datetime """

    
class IEsxVimDatacenter(IEsxVimObj):
    """
    The interface to the common container object for hosts and virtual
    machines. Every host and virtual machine must be under a distinct
    datacenter in the inventory, and datacenters may not be nested under
    other datacenters.
    """


class IEsxVimDatastore(IEsxVimObj):
    """
    Represents a storage location for virtual machine files. A storage
    location can be a VMFS volume, a directory on Network Attached Storage,
    or a local file system path.

    A datastore is platform-independent and host-independent. Therefore, 
    datastores do not change when the virtual machines they contain are 
    moved between hosts. The scope of a datastore is a datacenter;
    the datastore is uniquely named within the datacenter.
    """

class IEsxVimNetwork(IEsxVimObj):
    """
    Represents a network accessible by either hosts or virtual machines.
    This can be a physical network or a logical network, such as a VLAN.
    """

class IEsxVimFolder(IEsxVimObj):
    """
    These are generic folders for storing inventory objects.
    """

class IEsxVimVirtualMachine(IEsxVimObj):
    """
    VirtualMachine is the managed object type for manipulating virtual
    machines, including templates that can be deployed (repeatedly) as new
    virtual machines. This type provides methods for configuring and
    controlling a virtual machine.
    """
    def shutdown():
        """
        shutdown this esx object to an internal object
        """

    def convertobj():
        """
        converts this esx object to an internal object
        """

class IEsxVimHostSystem(IEsxVimObj):
    """
    Represents a set of physical compute resources for a set of virtual
    machines.
    """
    def values(self):
        '''See interface `IReadContainer`'''
