# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""implementation of a "esx_vim daemon" 
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.admin_utils.esx_vim.esx_vim_obj import EsxVimObj
from org.ict_ok.admin_utils.esx_vim.interfaces import \
     IEsxVimDatacenter


class EsxVimDatacenter(EsxVimObj):
    """
    The interface to the common container object for hosts and virtual
    machines. Every host and virtual machine must be under a distinct
    datacenter in the inventory, and datacenters may not be nested under
    other datacenters.
    """
    implements(IEsxVimDatacenter)
