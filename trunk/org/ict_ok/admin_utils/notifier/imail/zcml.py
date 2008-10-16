# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0602,W0232
#
"""
'mail' ZCML Namespaces Schemas
implementation of a "Object-Message-Queue-Utility" 
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.schema import BytesLine
from zope.sendmail.zcml import IMailerDirective
from zope.sendmail.interfaces import IMailer
from zope.component.zcml import handler

# ict_ok.org imports

class IAdmUtilEmailNotifierDirective(IMailerDirective):
    """Registers a new pseude mailer."""

    hostname = BytesLine(
        title=u"Hostname",
        description=u"Hostname of the SMTP host.",
        default="localhost",
        required=False)

def ikAdmUtilEmailNotifier(_context, name, hostname="localhost"):
    _context.action(
        discriminator = ('utility', IMailer, name),
        callable = handler,
        args = ('registerUtility',
                AdmUtilEmailNotifier(hostname), IMailer, name)
        )
