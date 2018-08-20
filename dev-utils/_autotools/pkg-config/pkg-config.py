# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/glib"] = "default"

    def setTargets(self):
        self.description = "pkg-config is a helper tool used when compiling applications and libraries"
        self.svnTargets['master'] = 'git://anongit.freedesktop.org/pkg-config'
        for ver in ["0.26", "0.29.2"]:
            self.targets[ver] = f"https://pkg-config.freedesktop.org/releases/pkg-config-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"pkg-config-{ver}"
        self.targetDigests["0.29.2"] = (['6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '0.29.2'


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        root = self.shell.toNativePath(CraftCore.standardDirs.craftRoot())
        self.subinfo.options.configure.args += (f" --disable-static --enable-shared"
                                                f" PKG_CONFIG=':'"
                                                f" GLIB_LIBS='-L{root}/lib -lglib-2.0 -liconv -lintl'"
                                                f" GLIB_CFLAGS='-I{root}/include/glib-2.0'")


    def createPackage(self):
        # TODO: reduce package size
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        return TypePackager.createPackage(self)
