import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.defaultTarget = '0.3.2'
        self.description = "a library to perform image correction based on lens profiles"

        for ver in ['0.2.6', '0.3.2']:
            self.targets[ver] = "https://github.com/lensfun/lensfun/archive/v%s.tar.gz" % (ver)
            self.targetInstSrc[ver] = "lensfun-%s" % ver

        self.targetDigests['0.2.6'] = 'ed20d5a04ff5785d15ea8e135bc125752d2d5a73'
        self.targetDigests['0.3.2'] = '1d978b15aa7304d66a4931fa37ca9f8f89396c16'

        self.patchToApply['0.2.6'] = ('lensfun-0.2.6.diff', 1)
        self.patchToApply['0.3.2'] = ('lensfun-0.3.2.patch', 1)

    def setBuildOptions(self):
        info.infoclass.setBuildOptions(self)

        self.options.configure.args = "-DBUILD_STATIC=OFF"
        self.options.configure.args += " -DBUILD_TESTS=OFF"
        self.options.configure.args += " -DBUILD_AUXFUN=OFF"
        self.options.configure.args += " -DBUILD_FOR_SSE=ON"
        self.options.configure.args += " -DBUILD_FOR_SSE2=ON"
        self.options.configure.args += " -DBUILD_DOC=OFF"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        # self.buildDependencies["dev-utils/doxygen"] = None
        self.runtimeDependencies['libs/glib'] = 'default'
        # self.runtimeDependencies['libs-bin/zlib']  = 'default' # only needed if building auxfun and tests
        # self.runtimeDependencies['libs-bin/libpng'] = 'default' # only needed if building auxfun and tests


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
