# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
#
"""implementation of browser class of Host object
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import form, field

# ict_ok.org imports
from org.ict_ok.components.host.special.vmware_vm.interfaces import \
     IHostVMwareVm
from org.ict_ok.components.host.special.vmware_vm.host import Host
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.components.host.browser.host import \
     HostDetails

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class MSubAddHost(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add VMware Virtual Machine')
    viewURL = 'add_host_vmware_vm.html'
    weight = 50

# --------------- forms ------------------------------------



class DetailsHostForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of net')
    fields = field.Fields(IHostVMwareVm).omit(*HostDetails.omit_viewfields)


class AddHostForm(AddForm):
    """Add form."""
    label = _(u'Add VMware Virtual Machine')
    fields = field.Fields(IHostVMwareVm).omit(*HostDetails.omit_addfields)
    factory = Host


class EditHostForm(EditForm):
    """ Edit form for host """
    form.extends(form.EditForm)
    label = _(u'VMware Virtual Machine Edit Form')
    fields = field.Fields(IHostVMwareVm).omit(*HostDetails.omit_editfields)
