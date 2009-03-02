# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=E0211,W0232
#
"""Interface of Object-Message-Queue-Utility"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Bool, Int, TextLine

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IAdmUtilIdChooser(Interface):
    """A id getter utility."""
    def getIdChoosers():
        """ get all id chooser
        """

class IIdChooser(Interface):
    """An id getter
    """
    wasUsed = Bool(
        title=_("Was used"),
        description=_("Id chooser was used and cannot be deleted"),
        default = False,
        readonly = False,
        required = True)

    counter = Int(
        min = 0,
        title = _("Counter"),
        default = 0,
        required = True)
    
    step = Int(
        min = 1,
        title = _("Step"),
        default = 1,
        required = True)
    
    format = TextLine(
        min_length = 2,
        max_length = 30,
        title = _("Format"),
        description = _("Format with %%d for no."),
        default = u"ID %05d",
        required = True)

#    def canBeDeleted():
#        """
#        a object can be deleted with normal delete permission
#        special objects can overload this for special delete rules
#        (e.g. IAdmUtilCatHostGroup)
#        return True or False
#        """
    def incrementId():
        """return a unique valid id string.
        """
