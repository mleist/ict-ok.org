# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0232,W0142,R0901
#
"""implementation of browser class of email-generator
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.notifier.imail.interfaces import \
     INotifierEmail, IEventIfNotifierEmail
from org.ict_ok.admin_utils.notifier.browser.notifier import \
     NotifierDetails

_ = MessageFactory('org.ict_ok')


class NotifierEmailDetails(NotifierDetails):
    """
    Browser details for email-generator
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikAuthor', 'ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

    def send_test(self):
        """
        will send a test message by the notifier
        """
        testMsg = """This is a test message from
        """
        self.context.send_test(testMsg)
        nextURL = self.request.get('nextURL', default=None)
        if nextURL:
            return self.request.response.redirect(nextURL)
        else:
            return self.request.response.redirect('./@@details.html')

    def getConfig(self):
        """Trigger configuration by web browser
        """
        return self.context.getConfig()

# --------------- forms ------------------------------------


class ViewNotifierEmailForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of email notifier')
    fields = field.Fields(INotifierEmail).omit(\
        *NotifierEmailDetails.omit_viewfields)


class EditNotifierEmailForm(EditForm):
    """ Edit for for net """
    label = _(u'edit email notifier')
    fields = field.Fields(INotifierEmail).omit(\
        *NotifierEmailDetails.omit_editfields)

class EditNotifierEmailEventIfForm(EditForm):
    """ Edit Event Interface of object """
    label = _(u'email notifier event interfaces form')
    fields = field.Fields(IEventIfNotifierEmail)
