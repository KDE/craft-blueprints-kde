# -*- coding: utf-8 -*-

import info
import utils
from CraftOS.osutils import OsUtils
from Package.AutoToolsPackageBase import AutoToolsPackageBase

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
            self.targets[version] = f"{PACKAGE_CRAN_MIRROR}{PACKAGE_PATH}R-{version}.tar.gz"
            self.targetInstSrc[version] = f"R-{version}"
        self.defaultTarget = "4.3.3"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--enable-R-shlib", "--with-readline=no", "--with-x=no"]
        # unfortunately, Craft's .debug files cause mis-behavior in R (it will then detect a multi-arch install with sub-architectures "R" and "R.debug"), so don't create those
        self.subinfo.options.package.disableStriping = True

    def configure(self):
        env = {}
        env["CFLAGS"] = "-I" + os.path.join(OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()), "include")  # Needed in R 4.3.3 to find zlib
        env["CPPFLAGS"] = env["CFLAGS"]
        env["LDFLAGS"] = "-L" + os.path.join(OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()), "lib")
        with utils.ScopedEnv(env):
            return super().configure()

    def install(self):
        res = super().install()
        for lib in ["libR.so", "libRlapack.so", "libRblas.so"]:
            res = res and utils.createSymlink(self.imageDir() / "lib/R/lib" / lib, self.imageDir() / "lib" / lib)
        return res
