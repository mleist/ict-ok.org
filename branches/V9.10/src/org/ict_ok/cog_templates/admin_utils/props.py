# -*- coding: utf-8 -*-
#
# Copyright (c) 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#

authors = [
   {r'name': r'Markus Leist',
    r'email': r'leist@ikom-online.de'},
    ]

filename = r'testmod'
longpath = r'org.ict_ok.admin_utils'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)

modulename = r'TestMod'
utilityname = r'AdmUtil' + modulename
loggername = r'AdmUtil' + modulename
utilitytitle = r'Test Utiltiy'

purpose = r"""test util

the test util should demonstrate the use of cog
"""

copyrights = [2006, 2007]
