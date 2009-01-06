# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#

# zope imports
from zope.schema import vocabulary

def AllRoomsVocab(obj):
    return vocabulary.SimpleVocabulary([])

def setUpAllRoomsVocab(test):
    vr = vocabulary.getVocabularyRegistry()
    vr.register('AllRoomsVocab', AllRoomsVocab)

