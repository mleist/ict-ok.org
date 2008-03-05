# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
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
from org.ict_ok.components.host.special.vmware_esx.interfaces import \
     IHostVMwareEsx, IEventIfHostVMwareEsx
from org.ict_ok.components.host.special.vmware_esx.host import Host
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DisplayForm, EditForm
from org.ict_ok.components.host.browser.host import \
     HostDetails
from org.ict_ok.components.host.browser.host import \
     EditEventHostEventIfForm as SuperEditEventIfForm

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class MSubAddHost(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add VMware ESX Server')
    viewURL = 'add_host_vmware_esx.html'
    weight = 50

# --------------- forms ------------------------------------


class DetailsHostForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of VMware ESX Server')
    fields = field.Fields(IHostVMwareEsx).omit(*HostDetails.omit_viewfields)


class AddHostForm(AddForm):
    """Add form."""
    label = _(u'Add VMware ESX Server')
    fields = field.Fields(IHostVMwareEsx).omit(*HostDetails.omit_addfields)
    factory = Host


class EditHostForm(EditForm):
    """ Edit form for host """
    form.extends(form.EditForm)
    label = _(u'VMware ESX Server Edit Form')
    fields = field.Fields(IHostVMwareEsx).omit(*HostDetails.omit_editfields)


class EditEventHostEventIfForm(SuperEditEventIfForm):
    """ Edit Event Interface of object """
    label = _(u'esx host event interfaces form')
    fields = field.Fields(IEventIfHostVMwareEsx)
    
