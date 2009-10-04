# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=
#

import urllib2
import re
import pickle
from BeautifulSoup import BeautifulSoup
from gzip import GzipFile
from pprint import pprint

# open file
dataFile = GzipFile("snmp_mrtg_data.gz", "rb")

# read from a gzipped pickle
all_templ_data = pickle.load(dataFile)
dataFile.close()

# pprint it
pprint(all_templ_data)
