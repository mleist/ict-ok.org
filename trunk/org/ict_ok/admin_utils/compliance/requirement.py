# -*- coding: utf-8 -*-
#
# Copyright (c) 2007, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
"""Interface of compliance utility

the compliance utility should store the compliance/requirement-templates
for the host- or service-instances
"""

__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.interface import implements
from zope import annotation
import zope.app.container.contained

# zc imports

# ict_ok.org imports
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.admin_utils.compliance.interfaces import \
     IRequirement
import schooltool.requirement.requirement
from schooltool.requirement.evaluation import getRequirementList

logger = logging.getLogger("AdmUtilCompliance")

REQUIREMENT_KEY = "org.ict_ok.admin_utils.compliance.requirement"


class Requirement(Superclass, schooltool.requirement.requirement.Requirement):
    """ ict-ok.org wrapper
    """
    implements(IRequirement)
    def __init__(self, title, **data):
        schooltool.requirement.requirement.Requirement.__init__(self, title)
        Superclass.__init__(self, ikName=title, **data)
        Superclass.__post_init__(self, **data)


def getRequirement(context):
    """Adapt an ``IHaveRequirement`` object to ``IRequirement``."""
    annotations = annotation.interfaces.IAnnotations(context)
    try:
        return annotations[REQUIREMENT_KEY]
    except KeyError:
        ## TODO: support generic objects without ikName
        requirement = Requirement(getattr(context, "ikName", None))
        annotations[REQUIREMENT_KEY] = requirement
        zope.app.container.contained.contained(
            requirement, context, u'++requirement++')
        return requirement
# Convention to make adapter introspectable
getRequirement.factory = Requirement
