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

filename = r'test'
longpath = r'org.ict_ok.components.service.special'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.service' % (filename)

#modulename = r'TestMod'
servicename = r'Test'
serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
servicetitle = r'%s Service' % servicename

purpose = r"""test service

A test service check object.
"""

copyrights = [2006, 2007, 2008]
