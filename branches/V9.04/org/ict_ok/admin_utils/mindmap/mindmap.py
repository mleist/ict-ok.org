# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <s.napiorkowski@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: cog_template.py_cog 273 2008-08-26 13:23:57Z markusleist $
#
# pylint: disable-msg=E1101,E0611
"""Interface of mind map util

the mind map util will display some information from ict-ok in form of a mind map
"""

__version__ = "$Id: cog_template.py_cog 273 2008-08-26 13:23:57Z markusleist $"

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
    
    def placeHolder(self):
        """ stupid place holder
        """
        return u"i'm not here"
