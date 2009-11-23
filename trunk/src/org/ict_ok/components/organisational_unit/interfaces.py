# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of OrganisationalUnit"""


__version__ = "$Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IOrganisationalUnit(Interface):
    """A OrganisationalUnit object."""

    name = TextLine(
        title = _(u'OrganisationalUnit name'),
        description = _(u"OrganisationalUnit name"),
        required = False)

    parent_O_OU = Choice(
        title = _(u'Parent'),
        vocabulary = 'AllOrganisationsAndOrganisationalUnits',
        required = False)

    subOUs = List(
        title = _(u'Sub organisational units'),
        value_type=Choice(vocabulary='AllValidSubOrganisationalUnits'),
        default=[],
        required = False)
        
#    def trigger_online():
#        """
#        trigger workflow
#        """


class IOrganisationalUnitFolder(Interface):
    """Container for OrganisationalUnit objects
    """


class IAddOrganisationalUnit(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllOrganisationalUnitTemplates",
        required = False)
