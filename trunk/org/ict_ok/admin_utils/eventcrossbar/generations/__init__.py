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
from zope.app.publication.zopepublication import ZopePublication

key = 'org.ict_ok.components.interface.generations'

AppSchemaManager = SchemaManager(
    minimum_generation = 1,
    generation = 1,
    package_name=key)

print "eventcrossbar.AppSchemaManager"

def getRootFolder(context):
    """ get root folder by ZopePublication """
    return context.connection.root().get(ZopePublication.root_name, None)
