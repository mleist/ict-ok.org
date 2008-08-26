# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Supernode

Superclass for node objects (containing objects) 

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.app.container.btree import BTreeContainer

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode
from org.ict_ok.components.superclass.superclass import Superclass


class Supernode(BTreeContainer, Superclass):
    """
    the supernode
    """

    implements(ISupernode)

    def __init__(self, **data):
        """
        constructor of Supernode
        """
        Superclass.__init__(self, **data)
        BTreeContainer.__init__(self)
        for (name, value) in data.items():
            if name in ISupernode.names():
                setattr(self, name, value)
        self.ikRevision = __version__
