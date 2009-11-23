# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""implementation of a "esx_vim daemon" 
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.admin_utils.esx_vim.esx_vim import globalEsxVimUtility
from org.ict_ok.admin_utils.esx_vim.esx_vim_obj import EsxVimObj
from org.ict_ok.admin_utils.esx_vim.interfaces import \
     IEsxVimHostSystem


class EsxVimHostSystem(EsxVimObj):
    """
    Represents a set of physical compute resources for a set of virtual
    machines.
    """
    implements(IEsxVimHostSystem)
    
    def values(self):
        '''See interface `IReadContainer`'''
        print "EsxVimHostSystem.values"
        return globalEsxVimUtility.get_EsxVimAllDict(self, self).values()

