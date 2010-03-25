# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=W0232
#
"""Interface of Object-Message-Queue-Utility"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, List

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IAdmUtilCategories(Interface):
    """A configuration utility."""
    def getNamedReqDict():
        """ all Reqs in Dict with ikName as key
        """


class ICategory(Interface):
    """A host group entry.
    """
#    components = List (
#        title = _("Components"),
#        value_type = Choice(
#            title = _("Component"),
#            description = _("Component."),
#            vocabulary="AllComponents",
#            required = False),
#        readonly = False,
#        required = False)

    components = List(
        title = _(u'Components'),
        description = _(u"Components"),
        value_type=Choice(vocabulary='AllComponents'),
        required = False)

    requirements = List(
        title = _(u'Requirements'),
        description = _(u"Requirements"),
        value_type=Choice(vocabulary='AllValid1stRequirementVocab'),
        required = False)
