# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""not specialized generator for configuration files
"""

__version__ = "$Id$"

# phython imports
import logging

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.generators.interfaces import \
     IAdmUtilGenerators

logger = logging.getLogger("AdmUtilGenerators")


class AdmUtilGenerators(Supernode):
    """Implementation of unspecified generator
    """

    implements(IAdmUtilGenerators)

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__
