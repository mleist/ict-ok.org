# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""
skin breadcrumbs interfaces
"""
__version__ = "$Id$"

# python imports

# zope imports
from zope.schema import TextLine, Bool, URI
from zope.interface import Interface, Attribute

# z3c imports

class IBreadcrumbs(Interface):
    """An object providing breadcrumbs.

    This object will use the ``IBreadcrumbInfo`` adapter to get its
    information from each entry.
    """

    crumbs = Attribute('An iteratable of all breadcrumbs.')

class IBreadcrumbInfo(Interface):
    """Provides pieces of information about a breadcrumb."""

    name = TextLine(
        title=u'Name',
        description=u'The name of the breadcrumb.',
        required=True)

    url = URI(
        title=u'URL',
        description=u'The url of the breadcrumb.',
        required=True)

    active = Bool(
        title=u'Active',
        description=u'Tells whether the breadcrumb link should active.',
        required=True,
        default=True)
