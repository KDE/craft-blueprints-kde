# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "a portable C library for accessing git repositories"
        self.svnTargets['master'] = 'https://github.com/libgit2/libgit2.git'

        # try to use latest stable libgit2
        ver = '1.1.0'
        self.targets[ver] = f"https://github.com/libgit2/libgit2/archive/v{ver}.tar.gz"
        self.archiveNames[ver] = f"libgit2-{ver}.tar.gz"
        self.targetInstSrc[ver] = f"libgit2-{ver}"
        self.targetDigests[ver] = (['41a6d5d740fd608674c7db8685685f45535323e73e784062cf000a633d420d1e'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies['dev-utils/pkg-config'] = 'default'
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies['libs/libssh2'] = 'default'
        self.runtimeDependencies['libs/pcre2'] = 'default'
        self.runtimeDependencies['libs/openssl'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += "-DBUILD_CLAR=OFF"
