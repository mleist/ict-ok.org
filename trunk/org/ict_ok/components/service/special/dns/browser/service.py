# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <->
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: service.py_cog 192 2008-03-18 17:08:45Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Dns Service"""

__version__ = "$Id: service.py_cog 192 2008-03-18 17:08:45Z markusleist $"

# phython imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.service.special.dns.interfaces import \
     IServiceDns
from org.ict_ok.components.service.special.dns.service import \
     Service
from org.ict_ok.skin.menu import GlobalMenuSubItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm
from org.ict_ok.components.service.browser.service import \
     ServiceDetails

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddService(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Dns check')
    viewURL = 'add_dns_service.html'
    weight = 50

# --------------- forms ------------------------------------


class AddServiceForm(AddForm):
    """Add form."""
    label = _(u'Add Dns Service Check')
    fields = field.Fields(IServiceDns).omit(*ServiceDetails.omit_addfields)
    factory = Service
