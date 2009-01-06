# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232,W0622
#
"""Interface of Cron-Utility"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.schema import TextLine, Choice
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')

import pytz


class IAdmUtilCron(ISupernode):
    """
    major component for registration and event distribution 
    """

    timezone = Choice(
        title=_("Time Zone"),
        description=_("Time Zone used to display your calendar"),
        values=pytz.common_timezones,
        required = False)

    def receiveCron(self, str_time):
        """receive cron signal
        """

    def getCronTime(self):
        """get last cron timestamp
        """


class IGlobalCronUtility(Interface):
    """
    IGlobalCronUtility
    """
    lastCron = TextLine(
        min_length = 5,
        max_length = 40,
        title = _("Last Cron Start"),
        description = _("Date of last Cron-Start"),
        default = _("00.00.0000"),
        required = True)
