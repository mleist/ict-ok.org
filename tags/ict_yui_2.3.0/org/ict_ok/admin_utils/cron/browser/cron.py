# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142,R0901
#
"""implementation of browser class of cron handler
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
from org.ict_ok.admin_utils.cron.interfaces import \
     IAdmUtilCron

_ = MessageFactory('org.ict_ok')


class AdmUtilCronDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    def getInstanceCounter(self):
        """convert instance counter for display
        """
        return self.context.getInstanceCounter()

    def getCronTime(self):
        """convert cron timestamp for display
        """
        return self.context.getCronTime()

# --------------- forms ------------------------------------

class ViewAdmUtilCronForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of cron')
    fields = field.Fields(IAdmUtilCron).omit(\
        *AdmUtilCronDetails.omit_viewfields)


class EditAdmUtilCronForm(EditForm):
    """ Edit for for net """
    label = _(u'edit cron')
    fields = field.Fields(IAdmUtilCron).omit(\
        *AdmUtilCronDetails.omit_editfields)

