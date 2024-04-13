# -*- coding: utf-8 -*-

import info

PACKAGE_CRAN_MIRROR = "https://ftp.gwdg.de/pub/misc/cran"
PACKAGE_PATH = "/src/base/R-4/"


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/pcre2"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/libcurl"] = None

    def setTargets(self):
        for version in ["4.3.3", "4.2.3"]:
            self.targets[version] = PACKAGE_CRAN_MIRROR + PACKAGE_PATH + "R-" + version + ".tar.gz"
            self.targetInstSrc[version] = "R-%s" % version
        self.defaultTarget = "4.3.3"


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--enable-R-shlib", "--with-readline=no", "--with-x=no"]
        self.subinfo.options.configure.cflags = "-I" + os.path.join(OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()), "include") + " -I" + os.path.join(OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()), "include", "curl")
        self.subinfo.options.configure.cxxflags = "-I" + os.path.join(OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()), "include") + " -I" + os.path.join(OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()), "include", "curl")
        self.subinfo.options.configure.ldflags = "-L" + os.path.join(OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()), "lib")
        # unfortunately, Craft's .debug files cause mis-behavior in R (it will then detect a multi-arch install with sub-architectures "R" and "R.debug"), so don't create those
        self.subinfo.options.package.disableStriping = True

    def install(self):
        res = super().install()
        for lib in ["libR.so", "libRlapack.so", "libRblas.so"]:
            res = res and utils.createSymlink(os.path.join(self.imageDir(), "lib", "R", "lib", lib), os.path.join(self.imageDir(), "lib", lib))
        return res
