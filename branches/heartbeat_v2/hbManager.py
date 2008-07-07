# -*- coding: utf-8 -*-
#
# Copyright (c) 2008,
#               Sebastian Napiorkowski
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""
"""

__version__ = "$Id$"

# phython imports
import hb_mini

class HbManager(object):
    """organizes multiple heartbeat manager 
    """
    def __init__(self):
        self.manager = {}

    def add_manager(self, cluster_id):
        self.manager[cluster_id] = hb_mini.miniManager()

    def del_manager(self, cluster_id):
        del(self.manager[cluster_id])