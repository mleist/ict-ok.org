# -*- coding: utf-8 -*-
#
import os
from setuptools import setup, find_packages

setup(name = "org.ict-ok",
      version = "9.10",
      description = "",
      author = "",
      author_email = "",
      license = "",
      package_dir = {'': 'src'},
      packages=find_packages('src'),
      include_package_data = True,
      zip_safe=False,
      extras_require = dict(
          app = ['zope.app.appsetup',
                 'zope.app.authentication',
                 'zope.app.container',
                 'zope.app.error',
                 'zope.app.form',
                 'zope.app.i18n',
                 'zope.app.publisher',
                 'zope.app.publication',
                 'zope.app.security',
                 'zope.app.securitypolicy',
                 'zope.app.twisted',
                 'zope.app.wsgi',
                 'zope.contentprovider',
                 'zope.site',
                 ],
          test = ['z3c.coverage',
                  'z3c.etestbrowser',
                  'zope.app.testing'],
          ),
    install_requires = [
        'setuptools',
#        'lxml',
#        'gocept.runner',
#        'gocept.objectquery',
#        'ldapadapter',
#        'ldappas',
#        'lovely.relation',
#        'schooltool.gradebook',
#        'pysnmp',
#        'pyasn1',
#        'pyxml',
#        'magnitude',
#        'pyExcelerator',
#        #'py-rrdtool',
#        'pyOpenSSL',
#        'z3c.csvvocabulary',
#        'z3c.form',
#        'z3c.formui',
#        'z3c.layer.pagelet',
#        'z3c.pagelet',
#        'z3c.template',
#        'z3c.zrtresource',
#        'z3c.breadcrumb',
#        'z3c.form',
#        'z3c.formui',
#        'z3c.i18n',
#        'z3c.layer',
#        'z3c.macro',
#        'z3c.menu',
#        'z3c.pagelet',
#        'z3c.template',
#        'z3c.viewlet',
#        #'z3c.rml',
#        'z3c.pt',
#        'z3c.blobfile',
#        'z3c.ptcompat',
#        #'z3c.pt.compat',
#        'z3c.reference',
#        'zc.resourcelibrary',
#        'zc.table',
#        'zc.queue',
#        'zc.resourcelibrary',
#        'zc.table',
#        'zc.i18n',
#        'zc.relation',
#        'zc.relationship<=1.999',
#        'zope.annotation',
#        'zope.app.apidoc',
#        'zope.app.container',
#        'zope.app.folder',
#        'zope.app.pagetemplate',
#        'zope.app.session',
#        'zope.app.wfmc',
#        'zope.app.zapi',
#        'zope.app.intid',
#        'zope.app.catalog',
#        'zope.app.keyreference',
#        'zope.app.pythonpage',
#        'zope.app.boston',
#        'zope.app.workflow',
##        'zope.app.pluggableauth',
#        'zope.component [zcml]',
#        'zope.interface',
#        'zope.location',
#        'zope.pagetemplate',
#        'zope.publisher',
#        'zope.rdb',
#        'zope.schema',
#        'zope.traversing',
#        'zope.viewlet',
#        'zope.sendmail',
#        'zope.xmlpickle',
        ],
      )