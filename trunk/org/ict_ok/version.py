#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
# $LastChangedDate$
# $LastChangedRevision$
#
# pylint: disable-msg=C0301,C0121
#
"""
Version information
"""

##
## Do 15 MÃ¤r 17:24:24 CET 2007
##

import re

__versMajor = "1"
__versMinor = "5pre"
__versId = "$Id$"
__versLastChangedDate = "$LastChangedDate$"
__versRevision = "$LastChangedRevision$"
__versAuthor = "$LastChangedBy$"
__versHeadURL = "$HeadURL$"

def getVersRevision():
    """ get actual revision """
    result = re.match("\$LastChangedRevision:\ (\d*)(.*)", __versRevision)
    if result:
        return result.group(1).strip()
    else:
        return "---"

def getIkVersion():
    """ get actual version string """
    return "%s.%s.%s" % (__versMajor, __versMinor, getVersRevision())


if __name__ == '__main__':
    print getIkVersion()
