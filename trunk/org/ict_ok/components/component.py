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
"""superclass for all content-objects
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict_ok.org imports
from org.ict_ok.components.interfaces import IComponent
from org.ict_ok.components.supernode.supernode import Supernode


class Component(Supernode):
    """
    the general component instance
    """

    implements(IComponent)
    isTemplate = FieldProperty(IComponent['isTemplate'])
    requirement = FieldProperty(IComponent['requirement'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Supernode.__init__(self, **data)
        #self.myFactory = str(self.__class__).split("'")[1]
        for (name, value) in data.items():
            if name in IComponent.names():
                setattr(self, name, value)
        if not hasattr(self, 'isTemplate'):
            self.isTemplate = False
        self.ikRevision = __version__

    def get_health(self):
        """
        output of health, 0-1 (float)
        !!!!!! has to be implemented by subclass !!!!!!
        """
        #raise Exception, 'Not implemented yet'
        return None
    
    def get_wcnt(self):
        """
        weighted count of accesses
        !!!!!! has to be implemented by subclass !!!!!!
        """
        #raise Exception, 'Not implemented yet'
        return None
