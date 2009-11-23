# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <->
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Http Service"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.service.special.http.interfaces import \
     IServiceHttp
from org.ict_ok.components.service.special.http.service import \
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
    title = _(u'Add Http check')
    viewURL = 'add_http_service.html'
    weight = 50

# --------------- forms ------------------------------------


class AddServiceForm(AddForm):
    """Add form."""
    label = _(u'Add Http Service Check')
    fields = field.Fields(IServiceHttp).omit(*ServiceDetails.omit_addfields)
    factory = Service
