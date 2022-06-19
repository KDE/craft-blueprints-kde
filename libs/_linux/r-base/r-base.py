# -*- coding: utf-8 -*-

import info

PACKAGE_CRAN_MIRROR = 'https://ftp.gwdg.de/pub/misc/cran'
PACKAGE_PATH = '/src/base/R-4/'


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None
        self.runtimeDependencies["libs/pcre2"] = None
        self.runtimeDependencies["libs/libbzip2"] = None

    def setTargets(self):
        for version in ['4.2.0', '4.1.2']:
            self.targets[version] = PACKAGE_CRAN_MIRROR + PACKAGE_PATH + 'R-' + version + '.tar.gz'
            self.targetInstSrc[version] = "R-%s" % version
        self.defaultTarget = '4.2.0'


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--enable-R-shlib", "--with-readline=no", "--with-x=no"]
