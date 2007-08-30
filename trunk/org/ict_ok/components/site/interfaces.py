# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of Site"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.schema import Bool, TextLine
from zope.i18nmessageid import MessageFactory
from zope.app.container.constraints import contains

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class ISite(ISupernode):
    """
    The interface of Site-objects
    """
    contains('org.ict_ok.components.site.interfaces.ISite')

    sitename = TextLine(
        max_length = 80,
        title = _("Sitename"),
        description = _("Name of the site."),
        default = _("mysite"),
        required = True)


class IIkDeleteConfirm(Interface):
    """ Confirm the delete """
    confirmed = Bool(
        title = _(u"Confirm"),
        description = _(u"please confirm"),
        default = False)
