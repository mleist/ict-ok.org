# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: __init__.py_cog 394 2009-01-06 15:12:30Z markusleist $
#
"""define the range of generations of IndustrialComputer"""

__version__ = "$Id: __init__.py 394 2009-01-06 15:12:30Z markusleist $"

# zope imports
from zope.app.generations.generations import SchemaManager

key = 'org.ict_ok.components.ipc.generations'

AppSchemaManager = SchemaManager(
    minimum_generation = 1,
    generation = 1,
    package_name=key)
