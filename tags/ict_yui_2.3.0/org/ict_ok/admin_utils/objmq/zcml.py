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
"""
'mail' ZCML Namespaces Schemas
implementation of a "Object-Message-Queue-Utility" 
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.schema import BytesLine
from zope.sendmail.zcml import IMailerDirective
from zope.sendmail.interfaces import IMailer
from zope.component.zcml import handler

# ict_ok.org imports
from org.ict_ok.admin_utils.objmq.objtransport import AdmUtilObjTransport

class IAdmUtilObjTransportDirective(IMailerDirective):
    """Registers a new pseude mailer."""

    hostname = BytesLine(
        title=u"Hostname",
        description=u"Hostname of the SMTP host.",
        default="localhost",
        required=False)

def admUtilObjTransport(_context, name, hostname="localhost"):
    _context.action(
        discriminator = ('utility', IMailer, name),
        callable = handler,
        args = ('registerUtility',
                AdmUtilObjTransport(hostname), IMailer, name)
        )
