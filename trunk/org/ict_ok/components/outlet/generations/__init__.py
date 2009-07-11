# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""define the range of generations of Outlet"""

__version__ = "$Id$"

# zope imports
from zope.app.generations.generations import SchemaManager

key = 'org.ict_ok.components.outlet.generations'

AppSchemaManager = SchemaManager(
    minimum_generation = 1,
    generation = 1,
    package_name=key)
