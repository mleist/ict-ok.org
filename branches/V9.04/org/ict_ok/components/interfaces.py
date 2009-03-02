# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0211,W0232
#
"""Interface of host object"""

__version__ = "$Id$"

# zope imports
from zope.interface import Attribute, Interface
from zope.schema import Bool, Bytes, Choice, List
from zope.i18nmessageid import MessageFactory
from zope.app.folder.interfaces import IFolder

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.interfaces import ISupernode

_ = MessageFactory('org.ict_ok')


class IComponent(Interface):
    """A general component object."""

    myFactory = Attribute("Factory String of this object")
    ikRevision = Attribute("Class-Revision of this object")
    
    isTemplate = Bool(
        title = _("Object is template"),
        description = _("object is a template"),
        default = False,
        required = False)

#    requirement = Choice(
#        title = _("Requirement"),
#        description = _("The Requirement."),
#        vocabulary="AllRequirementVocab",
#        required = False)

    requirements = List (
        title = _("Requirements"),
        value_type = Choice(
            title = _("Requirement"),
            description = _("Requirement."),
            vocabulary="AllRequirementVocab",
            required = False),
        readonly = False,
        required = False)
    
    def get_health():
        """
        output of health, 0-1 (float)
        !!!!!! has to be implemented by subclass !!!!!!
        """

    def get_wcnt():
        """
        weighted count of accesses
        !!!!!! has to be implemented by subclass !!!!!!
        """


class IComponentFolder(ISuperclass, IFolder):
    """Container for MobilePhone objects
    """

        
class IImportXlsData(Interface):
    """Interface for all Objects"""
    xlsdata = Bytes(
        title = _("XLS data"),
        required = True)
    
    codepage = Choice(
        title = _("Codepage"),
        description = _("Codepage of XLS"),
        vocabulary="AllXlsCodepages",
        default = 'cp850',
        required = True)


class IImportCsvData(Interface):
    """Interface for all Objects"""
    csvdata = Bytes(
        title = _("CSV data"),
        required = True)


