# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0232
#
"""implementation of browser class of demo1-generator
"""

__version__ = "$Id$"

# phython imports

# zope imports


class AdmUtilDemo1Details:
    """
    Browser details for demo1-generator
    """

    def getConfig(self):
        """Trigger configuration by web browser
        """
        return self.context.getConfig()
