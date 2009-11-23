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
"""Interface of Script"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope.interface import Attribute
from zope.schema import Text
from zope.app.folder.interfaces import IFolder

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class IScript(IComponent):
    """A service object."""

    pythonScript = Text(
        title = _("Python"),
        description = _("Python script."),
        default = u"",
        required = False)

    printHistory = Attribute("script print history list")
