# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 424 2009-02-02 23:58:56Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of HardwareAppliance"""


__version__ = "$Id: interfaces.py_cog 424 2009-02-02 23:58:56Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Date, Int, TextLine

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IHardwareAppliance(Interface):
    """A HardwareAppliance object."""

    def trigger_online():
        """
        trigger workflow
        """


class IHardwareApplianceFolder(Interface):
    """Container for HardwareAppliance objects
    """


class IAddHardwareAppliance(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllHardwareApplianceTemplates",
        required = False)
