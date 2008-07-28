# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of Script

Script does ....

"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.script.interfaces import IScript


class Script(Component):
    """
    the template instance
    """

    implements(IScript)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    pythonScript = FieldProperty(IScript['pythonScript'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        for (name, value) in data.items():
            if name in IScript.names():
                setattr(self, name, value)
        self.ikRevision = __version__
