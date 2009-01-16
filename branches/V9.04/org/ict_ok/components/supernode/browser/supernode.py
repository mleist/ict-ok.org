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
"""implementation of Supernode

Superclass for node objects (containing objects) 

"""

__version__ = "$Id$"

# python imports

# zope imports

# ict_ok.org imports
from org.ict_ok.components.superclass.browser.superclass import \
     SuperclassDetails

# --------------- menu entries -----------------------------


# --------------- forms ------------------------------------


# --------------- object details ---------------------------


class SupernodeDetails(SuperclassDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SuperclassDetails.omit_viewfields + []
    omit_addfields = SuperclassDetails.omit_addfields + []
    omit_editfields = SuperclassDetails.omit_editfields + []
