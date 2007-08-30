# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0612
#
"""implementation of a "Object-Message-Queue-Utility" 
"""

__version__ = "$Id$"

# phython imports
import logging

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.admin_utils.notifier.email.interfaces import IAdmUtilEmailNotifier

logger = logging.getLogger("AdmUtilEmailNotifier")


class AdmUtilEmailNotifier(object):
    """A pseudo-mailer that delivers objects by mail."""

    implements(IAdmUtilEmailNotifier)

    def __init__(self, hostname='localhost'):
        self.hostname = hostname

    def send(self, fromaddr, toaddrs, message):
        """
        send object data as faked e-mail
        """
        logger.info(u"AdmUtilEmailNotifier.msg: %s (%s)->(%s)" % \
                    (message, fromaddr, toaddrs))
        #a = 1 / 0

        