# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0613,W0232,W0201,W0142,W0107
#
"""implementation of browser class of IkSite object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# zc imports

# z3c imports
from z3c.form import field

# ict-ok.org imports
from org.ict_ok.components.supernode.browser.supernode import SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import DisplayForm
from org.ict_ok.admin_utils.reports.interfaces import IAdmUtilReports


_ = MessageFactory('org.ict_ok')


# --------------- helper functions -------------------------

# --------------- menu entries -----------------------------

# --------------- object details ---------------------------

class AdmUtilReportsDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']


# --------------- forms ------------------------------------

class DetailsAdmUtilReportsForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of reports')
    fields = field.Fields(IAdmUtilReports).omit(\
        *AdmUtilReportsDetails.omit_viewfields)
