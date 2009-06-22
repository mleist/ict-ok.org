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
# pylint: disable-msg=E1101,E0611
"""Interface of mind map util

the mind map util will display some information from ict-ok in form of a mind map
"""

__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# zc imports

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.mindmap.interfaces import \
     IAdmUtilMindMap

logger = logging.getLogger("AdmUtilMindMap")


class AdmUtilMindMap(Supernode):
    """MindMap Utiltiy
    """
    
    implements(IAdmUtilMindMap)

    version = FieldProperty(IAdmUtilMindMap['version'])

    def __init__(self, **data):
        """
        constructor of Supernode
        """
        Supernode.__init__(self, **data)
        self.context = None
        self.ikRevision = __version__
    
    def placeHolder(self):
        """ stupid place holder
        """
        if self.context is not None:
            return u"%s is not here" % (self.context.ikName)
        else:
            return u"I'm not here"
