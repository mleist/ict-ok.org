# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface to email notifier"""

__version__ = "$Id$"

# zope imports
from zope.schema import TextLine, Int
from zope.sendmail.interfaces import IMailer
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.admin_utils.notifier.interfaces import \
     INotifier

_ = MessageFactory('org.ict_ok')


class INotifierEmail(INotifier, IMailer):
    """
    component for notifying with email
    """
    hostname = TextLine(
        title=_(u"Hostname/IP"),
        description=_(u"Name or IP of server to be used as SMTP server"),
        default = _('0.0.0.0'))
    
    portServer = Int(
        min = 1,
        max = 65535,
        title = _("SMTP serverport"),
        description = _("Port of the smtp server"),
        default = 25,
        required = True)

    from_addr = TextLine(
        title=_(u"'From:' address"),
        description=_(u"The e-mail address, and optionally the name of the sender"),
        default = _('alert@your.domain.com'),
        required = True)

#class IAdmUtilEmailNotifier(IMailer):
    #"""A pseudo-mailer that delivers objects by xmlrpc."""

    #hostname = TextLine(
        #title=_(u"Hostname"),
        #description=_(u"Name of server to be used as SMTP server."))
