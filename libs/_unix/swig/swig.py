# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/swig/swig.git'

        self.defaultTarget = 'master'
        self.description = "SWIG"
        self.displayName = "SWIG"

    def setDependencies(self):
        self.buildDependencies["dev-utils/bison"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
