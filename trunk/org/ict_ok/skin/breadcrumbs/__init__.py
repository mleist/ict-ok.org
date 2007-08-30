# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1111,E1101,E0611,W0232
#
"""
python package
"""
__version__ = "$Id$"

# zope imports
from zope.interface import Interface, implements, providedBy
from zope.component import adapts
from zope.contentprovider.interfaces import IContentProvider
from zope.app import zapi
import zope.interface
import zope.publisher.interfaces.http
from zope.traversing.interfaces import IContainmentRoot
from zope.publisher import browser
from zope.viewlet import viewlet

# z3c imports
from z3c.pagelet.browser import BrowserPagelet
from z3c.breadcrumb.browser import CustomNameBreadcrumb

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.breadcrumbs.interfaces import IBreadcrumbs,\
     IBreadcrumbInfo

class Breadcrumbs(browser.BrowserView):
    """Special Breadcrumbs implementation."""
    implements(IBreadcrumbs)

    @property
    def crumbs(self):
        try:
            myobjects = [self.context] + list(zapi.getParents(self.context))
        except Exception:
            myobjects = []
        myobjects.reverse()
        for myobject in myobjects:
            info = zapi.getMultiAdapter((myobject, self.request),
                                        IBreadcrumbInfo)
            yield {'name': info.name, 'url': info.url, 'active': info.active}


class GenericBreadcrumbInfo(object):
    """A generic breadcrumb info adapter."""
    implements(IBreadcrumbInfo)
    adapts(zope.interface.Interface,
           zope.publisher.interfaces.http.IHTTPRequest)

    # See interfaces.IBreadcrumbInfo
    active = True

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def name(self):
        """See interfaces.IBreadcrumbInfo"""
        try:
            name = IBrwsOverview(self.context).getTitle()
        except TypeError:
            name = getattr(self.context, 'title', None)
        if name is None:
            name = getattr(self.context, '__name__', None)
        if name is None and IContainmentRoot.providedBy(self.context):
            name = 'top'
        return name

    @property
    def url(self):
        """See interfaces.IBreadcrumbInfo"""
        return zapi.absoluteURL(self.context, self.request)
