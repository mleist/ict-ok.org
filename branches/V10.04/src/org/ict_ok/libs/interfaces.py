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
"""Interface of Codetemplate"""

__version__ = "$Id$"

# zope imports
from zope.interface import Attribute, Interface
from zope.schema import TextLine
from zope.i18nmessageid import MessageFactory

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass

_ = MessageFactory('org.ict_ok')


class IDocument(Interface):
    """A file object."""


class IDocumentAddable(Interface):
    """Document can be Add"""

