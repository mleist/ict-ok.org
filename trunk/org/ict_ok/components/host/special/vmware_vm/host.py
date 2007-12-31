# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict_ok.org imports
from org.ict_ok.components.host.special.vmware_vm.interfaces import \
     IHostVMwareVm, IEventIfHostVMwareVm
from org.ict_ok.components.host.host import Host as HostBase

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
        # find our correct factory, is there a better solution?
        for (fact_name, fact_obj) in zapi.getFactoriesFor(IHostVMwareVm):
            if (len(fact_name) > 11) and (fact_name[:11]=='org.ict_ok.'):
                self.myFactory = unicode(fact_name)
        for (name, value) in data.items():
            if name in IHostVMwareVm.names() or \
               name in IEventIfHostVMwareVm.names():
                setattr(self, name, value)

    def poweroff(self):
        """
        trigger poweroff
        """
        print "poweroff@browser"
        self.context.poweroff()
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def poweroff(self):
        """
        trigger poweroff
        """
        print "poweroff"
        
    def poweron(self):
        """
        trigger poweron
        """
        print "poweron"
