#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#

PYTHON=/usr/bin/python2.4
CWD=`pwd`
COG=/usr/bin/cog.py

all:
	@echo "generator make:"
	@echo "\tmake gen"
	@echo "\t\twill generate all files from cog-templates"
	@echo "\tmake clean"
	@echo "\t\twill clean all cog-templates"

gen:	configure.zcml \
	bootstrap.py \
	cog_template.py \
	__init__.py \
	interfaces.py \
	security.zcml \
	browser/cog_template.py \
	browser/configure.zcml \
	browser/__init__.py \
	browser/adapter/__init__.py

clean:
	@find . -type f -name \*_cog -exec rm -v {} \;

%.py : %.py_cog
	$(COG) -d -o $@ $<

%.zcml : %.zcml_cog
	$(COG) -d -o $@ $<

%.txt : %.txt_cog
	$(COG) -d -o $@ $<
