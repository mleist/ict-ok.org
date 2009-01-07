#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#

PYTHON=/usr/bin/python2.4
CWD=`pwd`
COG=cog.py
FILENAME_SH=`./props.py`
FILENAME=$(shell ./props.py)

all:
	@echo "generator make:"
	@echo "\tmake rename (do 1st)"
	@echo "\t\twill rename some cog-templates"
	@echo "\tmake gen (do 2nd)"
	@echo "\t\twill generate all files from cog-templates"
	@echo "\tmake allclean"
	@echo "\t\twill clean all cog-templates"

gen:	configure.zcml \
	__init__.py \
	interfaces.py \
	${FILENAME} \
	bootstrap.py \
	browser/${FILENAME} \
	browser/configure.zcml \
	browser/__init__.py \
	generations/evolve1.py \
	generations/configure.zcml \
	generations/__init__.py \
	ftests/__init__.py \
	adapter/__init__.py \
	adapter/rpt_pdf.py \
	adapter/search.py \
	adapter/state.py

clean:	rm -v configure.zcml
	rm -v __init__.py
#	interfaces.py \
#	${FILENAME} \
#	bootstrap.py \
#	browser/${FILENAME} \
#	browser/configure.zcml \
#	browser/__init__.py \
#	generations/evolve1.py \
#	generations/configure.zcml \
#	generations/__init__.py \
#	ftests/__init__.py \
#	adapter/__init__.py \
#	adapter/rpt_pdf.py \
#	adapter/search.py \
#	adapter/state.py

gen2:	configure.zcml \
	ftests/__init__.py \
	generations/configure.zcml \
	generations/evolve1.py \
	bootstrap.py \
	adapter/__init__.py \
	adapter/rpt_pdf.py \
	adapter/search.py \
	adapter/state.py \
	${FILENAME} \
	browser/${FILENAME}

allclean:
	@find . -type f -name \*_cog -exec rm -v {} \;

rename:
	cp template.py_cog $(FILENAME_SH)_cog
	cp browser/template.py_cog browser/$(FILENAME_SH)_cog

%.py : %.py_cog
	$(COG) -d -o $@ $<

%.zcml : %.zcml_cog
	$(COG) -d -o $@ $<

%.txt : %.txt_cog
	$(COG) -d -o $@ $<
