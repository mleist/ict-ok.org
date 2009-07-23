# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <s.napiorkowski@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0211,W0232,W0622
#
"""Interface of mac address db util

the mac address db util will display some information from ict-ok in form of a mac address db
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.schema import TextLine
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class IAdmUtilMacAddressDb(ISupernode):
    """MacAddressDb Utiltiy
    """
    version = TextLine(
        title = _("mac address db version"),
        description = _("mac address dbs must have a version."),
        readonly = False,
        required = False)

    def placeHolder():
        """ stupid place holder
        """
