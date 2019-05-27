# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/libgit2/libgit2.git'

        for ver in ['0.28.1']:
            self.targets[ver] = f"https://github.com/libgit2/libgit2/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"libgit2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libgit2-{ver}"
        self.patchToApply["0.28.1"] = [ ("libgit2-0.28.1-20190216.diff", 1)]
        self.targetDigests["0.28.1"] = (['0ca11048795b0d6338f2e57717370208c2c97ad66c6d5eac0c97a8827d13936b'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["0.28.1"] = 3

        self.description = "a portable C library for accessing git repositories"
        self.defaultTarget = '0.28.1'

    def setDependencies(self):
        self.buildDependencies['dev-utils/pkg-config'] = 'default'
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies['libs/iconv'] = 'default'
        self.runtimeDependencies['libs/libssh2'] = 'default'
        self.runtimeDependencies['libs/openssl'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += "-DUSE_ICONV=ON -DBUILD_CLAR=OFF"
