# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.targetDigests['3.7.0'] = '73adf9fdca5086dd47a32b34a398d2c1d492d18e'

        for ver in self.svnTargets.keys() | self.targets.keys():
            self.patchToApply[ver] = [("fix_shortpath.patch", 1), ("0041-libcxx-add-support-for-mingw-w64.patch", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/llvm-meta/clang"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = '-DCMAKE_CXX_FLAGS="-D_LIBCPP_HAS_NO_CONSTEXPR" -DLIBCXX_ENABLE_SHARED=OFF '
