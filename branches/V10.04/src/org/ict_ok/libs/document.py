# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0613,W0142
#
"""implementation of Superclass

Superclass for non containing objects 

"""

__version__ = "$Id$"


# zope imports
from zope.interface import implements

# z3c imports
from z3c.blobfile.file import File

# ict_ok.org imports
from org.ict_ok.libs.interfaces import IDocument
from org.ict_ok.components.superclass.superclass import Superclass

class Document(Superclass, File):
    implements(IDocument)

