# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: __init__.py 147M 2009-04-16 11:09:07Z (lokal) $
#
"""define the range of generations
"""

__version__ = "$Id: __init__.py 147M 2009-04-16 11:09:07Z (lokal) $"

# zope imports
from zope.app.generations.generations import SchemaManager

key = 'org.ict_ok.components.ipnet.generations'

AppSchemaManager = SchemaManager(
    minimum_generation = 2,
    generation = 2,
    package_name=key)
