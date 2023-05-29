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
        self.patchToApply['1.1.0'] = [("libgit2-pcre2-debugsuffix.diff", 1)]
        self.patchLevel[self.defaultTarget] = 1

    def setDependencies(self):
        self.buildDependencies['dev-utils/pkg-config'] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies['libs/libssh2'] = None
        self.runtimeDependencies['libs/pcre2'] = None
        self.runtimeDependencies['libs/openssl'] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        # ensure the more recent PCRE2 is used, per default it will pick up PCRE1 if found otherwise
        self.subinfo.options.configure.args += "-DBUILD_CLAR=OFF -DREGEX_BACKEND=pcre2"
