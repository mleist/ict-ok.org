# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: __init__.py_cog 506 2009-04-30 14:24:56Z markusleist $
#
"""define the range of generations of Contract"""

__version__ = "$Id: __init__.py_cog 506 2009-04-30 14:24:56Z markusleist $"

# zope imports
from zope.app.generations.generations import SchemaManager

key = 'org.ict_ok.components.contract.generations'

AppSchemaManager = SchemaManager(
    minimum_generation = 1,
    generation = 1,
    package_name=key)
