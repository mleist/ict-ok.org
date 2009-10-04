# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0613,W0232,W0201,W0142,C0111,R0901,R0201
#
"""implementation of browser class of IkSite object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory


# zc imports

# ict-ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.snmpd.snmpd import AdmUtilSnmpd

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------

# --------------- object details ---------------------------


class AdmUtilSnmpdDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']
    
    def test(self):
        zzz = self.context
        print "ZU:", zzz
        return "zulu"


# --------------- forms ------------------------------------

class DetailsAdmUtilSnmpdForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of snmpd')
    factory = AdmUtilSnmpd
    omitFields = AdmUtilSnmpdDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class EditAdmUtilSnmpdForm(EditForm):
    """ Edit for for site """
    label = _(u'edit snmpd settings')
    factory = AdmUtilSnmpd
    omitFields = AdmUtilSnmpdDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
