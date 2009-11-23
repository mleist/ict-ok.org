# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""define the range of generations of MobilePhone"""

__version__ = "$Id$"

# zope imports
from zope.app.generations.generations import SchemaManager

key = 'org.ict_ok.components.mobilephone.generations'

AppSchemaManager = SchemaManager(
    minimum_generation = 1,
    generation = 1,
    package_name=key)
