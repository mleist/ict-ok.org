# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""implementation of widget for physical values
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.component import getMultiAdapter
from zope.app.form.interfaces import IInputWidget
from zope.app.form.browser.widget import SimpleInputWidget

# ict_ok.org imports

class PhysicalWidget(SimpleInputWidget):
    
    def _getFormInput(self):
        value = super(PhysicalWidget, self)._getFormInput()
        if value is None:
            value = []
        if not isinstance(value, list):
            value = [value]
        return value
    
    def hasInput(self):
        return(self.name + '.marker') in self.request.form
    
    def hidden(self):
        s=''
        for value in self._getFormValue():
            widget = getMultiAdapter((self.context.value_type,
                                       self.request), IInputWidget)
            widget.name = self.name
            widget.setRenderedValue(value)
            s += widget.hidden()
        return s