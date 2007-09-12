# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=W0232
#
"""Interface of Object-Message-Queue-Utility"""

__version__ = "$Id$"

# zope imports

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import ISupernode


class IAdmUtilTicker(ISupernode):
    """A pseudo-mailer that delivers objects by xmlrpc."""
