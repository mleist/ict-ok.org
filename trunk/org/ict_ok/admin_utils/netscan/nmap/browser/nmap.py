# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0232,W0142,R0901
#
"""implementation of browser class of nmap-generator
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.netscan.nmap.interfaces import \
     IAdmUtilNMap

_ = MessageFactory('org.ict_ok')


class AdmUtilNMapDetails(SupernodeDetails):
    """
    Browser details for nmap-generator
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    def getConfig(self):
        """Trigger configuration by web browser
        """
        return self.context.getConfig()


# --------------- forms ------------------------------------


class ViewAdmUtilNMapForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of nmap scanner')
    fields = field.Fields(IAdmUtilNMap).omit(\
        *AdmUtilNMapDetails.omit_viewfields)


class EditAdmUtilNMapForm(EditForm):
    """ Edit for for net """
    label = _(u'edit nmap scanner')
    fields = field.Fields(IAdmUtilNMap).omit(\
        *AdmUtilNMapDetails.omit_editfields)
