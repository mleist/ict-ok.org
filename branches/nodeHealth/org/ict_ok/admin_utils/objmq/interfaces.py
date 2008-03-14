# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=E0213,W0232,W0622
#
"""Interface of Object-Message-Queue-Utility"""

__version__ = "$Id$"

# zope imports
from zope.schema import TextLine
from zope.i18nmessageid import MessageFactory
from zope.sendmail.interfaces import IMailer

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class IAdmUtilObjMQ(ISupernode):
    """
    component for message queueing between object of different instances
    """

class IAdmUtilObjTransport(IMailer):
    """A pseudo-mailer that delivers objects by xmlrpc."""

    hostname = TextLine(
        title=_(u"Hostname"),
        description=_(u"Name of server to be used as SMTP server."))
