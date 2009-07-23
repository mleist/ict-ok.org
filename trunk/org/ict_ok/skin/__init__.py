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
skin classes
"""
__version__ = "$Id$"

# python imports

# zope imports
from zope.component import queryUtility

# z3c imports

# ict_ok.org imports
from org.ict_ok.admin_utils.usermanagement.interfaces import \
     IAdmUtilUserManagement

class SkinDetails:
    def switch(self):
        """
        will switch the init view from user props
        """
#        nextURL = self.request.get('nextURL', default=None)
#        if nextURL:
#            return self.request.response.redirect(nextURL)
#        else:
        try:
            userManagement = queryUtility(IAdmUtilUserManagement)
            if userManagement is not None:
                redirectString = "./@@%s" % userManagement.startView
                return self.request.response.redirect(redirectString)
            else:
                return self.request.response.redirect('./@@overview.html')
        except:
            return self.request.response.redirect('./@@overview.html')
