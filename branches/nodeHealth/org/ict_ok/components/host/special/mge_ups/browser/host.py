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
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.host.special.mge_ups.interfaces import \
     IHostMgeUps, IEventIfHostMgeUps
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.components.host.special.mge_ups.host import Host
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm
from org.ict_ok.components.host.browser.host import \
     HostDetails

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------


class MSubAddHost(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add MGE UPS')
    viewURL = 'add_host_mge_ups.html'
    weight = 50

# --------------- forms ------------------------------------


class AddHostForm(AddForm):
    """Add form."""
    label = _(u'Add MGE UPS')
    fields = field.Fields(IHostMgeUps).omit(*HostDetails.omit_addfields)
    factory = Host

class EditHostEventIfForm(EditForm):
    """ Edit Event Interface of object """
    label = _(u'HostMgeUps Event Interfaces Form')
    fields = field.Fields(IEventIfHostMgeUps)
