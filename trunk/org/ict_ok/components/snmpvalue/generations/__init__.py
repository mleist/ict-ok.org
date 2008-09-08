# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""define the range of generations
"""

__version__ = "$Id$"

# zope imports
from zope.app.generations.generations import SchemaManager

key = 'org.ict_ok.components.snmpvalue.generations'

AppSchemaManager = SchemaManager(
    minimum_generation = 3,
    generation = 3,
    package_name=key)
