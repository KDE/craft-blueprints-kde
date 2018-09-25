# -*- coding: utf-8 -*-
import info
from Package.MSBuildPackageBase import *
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        # do not build under macOS; there's already a system iconv lib
        # if using a self-built iconv, we may run into issues like this:
        #   dyld: Symbol not found: _iconv
        #      Referenced from: /usr/lib/libcups.2.dylib
        #      Expected in: /Users/packaging/Craft/BinaryFactory/macos-64-clang/lib/libiconv.2.dylib
        #     in /usr/lib/libcups.2.dylib
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotMacOS

    def setTargets(self):
        for ver in ['1.15']:
            self.targets[ver] = 'https://ftp.gnu.org/pub/gnu/libiconv/libiconv-%s.tar.gz' % ver
            self.targetInstSrc[ver] = "libiconv-%s" % ver
        self.targetDigests['1.15'] = (['ccf536620a45458d26ba83887a983b96827001e92a13847b45e4925cc8913178'], CraftHash.HashAlgorithm.SHA256)

        self.description = "GNU internationalization (i18n)"
        self.defaultTarget = '1.15'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
