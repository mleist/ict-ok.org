# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of host object

host object represents a VMware Virtual Machine
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.component import queryUtility
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict_ok.org imports
from org.ict_ok.components.host.special.vmware_vm.interfaces import \
     IHostVMwareVm, IEventIfHostVMwareVm
from org.ict_ok.components.host.host import Host as HostBase
from org.ict_ok.admin_utils.esx_vim.interfaces import IAdmUtilEsxVim

class Host(HostBase):
    """
    the VmWare virtual machine instance
    """
    implements(IHostVMwareVm, IEventIfHostVMwareVm)

    esxUuid = FieldProperty(IHostVMwareVm['esxUuid'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        HostBase.__init__(self, **data)
        for (name, value) in data.items():
            if name in IHostVMwareVm.names() or \
               name in IEventIfHostVMwareVm.names():
                setattr(self, name, value)
        self.ikRevision = __version__

    def poweroff(self):
        """
        trigger poweroff
        """
        print "poweroff"
        esx_utility = queryUtility(IAdmUtilEsxVim)
        if esx_utility and len(self.esxUuid) > 0:
            esx_utility.powerOffVm(self.esxUuid)
        
    def poweron(self):
        """
        trigger poweron
        """
        print "poweron"
        esx_utility = queryUtility(IAdmUtilEsxVim)
        if esx_utility and len(self.esxUuid) > 0:
            esx_utility.powerOnVm(self.esxUuid)

    def eventInp_shutdown(self, eventMsg=None):
        """ start the shutdown of the host """
        eventMsg.stopit(self, "Host.eventInp_shutdown")
        print "Host.eventInp_shutdown (%s)              ############## <-" % (self.ikName)
        self.poweroff()

