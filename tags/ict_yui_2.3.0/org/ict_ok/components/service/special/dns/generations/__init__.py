# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <->
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: __init__.py_cog 192 2008-03-18 17:08:45Z markusleist $
#
"""define the range of generations
"""

__version__ = "$Id: __init__.py_cog 192 2008-03-18 17:08:45Z markusleist $"

# zope imports
from zope.app.generations.generations import SchemaManager

key = 'org.ict_ok.components.service.special.dns.generations'

AppSchemaManager = SchemaManager(
    minimum_generation = 1,
    generation = 1,
    package_name=key)
