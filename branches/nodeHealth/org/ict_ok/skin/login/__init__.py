# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""
python package
"""
__version__ = "$Id$"

# phython imports

# zope imports
from zope import component
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.security.interfaces import IAuthentication
from zope.app.security.browser.auth import HTTPAuthenticationLogout, \
     IUnauthenticatedPrincipal, HTTPAuthenticationLogin
from zope.app.security.interfaces import ILogout, ILogoutSupported

# z3c imports
from z3c.pagelet.browser import BrowserPagelet

# ict_ok.org imports


class AuthenticationLogout(BrowserPagelet, HTTPAuthenticationLogout):
    """ overloaded logout """
    confirmation = ViewPageTemplateFile('logout.pt')
    redirect = ViewPageTemplateFile('redirect.pt')
    def __init__(self, context, request):
        HTTPAuthenticationLogout.__init__(self, context, request)
        BrowserPagelet.__init__(self, context, request)
        
    def update(self):
        """set values for pagelet"""
        BrowserPagelet.update(self)
        if not IUnauthenticatedPrincipal.providedBy(self.request.principal):
            auth = component.getUtility(IAuthentication)
            ILogout(auth).logout(self.request)
        if 'nextURL' in self.request:
            self.request.response.redirect(self.request['nextURL'])


class AuthenticationLogin(BrowserPagelet, HTTPAuthenticationLogin):
    """ overloaded login """
    def __init__(self, context, request):
        HTTPAuthenticationLogin.__init__(self, context, request)
        BrowserPagelet.__init__(self, context, request)
    def update(self):
        """set values for pagelet"""
        BrowserPagelet.update(self)
        if IUnauthenticatedPrincipal.providedBy(self.request.principal):
            component.getUtility(IAuthentication).unauthorized(
                self.request.principal.id, self.request)
