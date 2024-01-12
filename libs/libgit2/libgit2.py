# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "a portable C library for accessing git repositories"
        self.svnTargets["master"] = "https://github.com/libgit2/libgit2.git"

        # try to use latest stable libgit2
        for ver in ["1.7.1"]:
            self.targets[ver] = f"https://github.com/libgit2/libgit2/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"libgit2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libgit2-{ver}"

        self.targetDigests["1.7.1"] = (["17d2b292f21be3892b704dddff29327b3564f96099a1c53b00edc23160c71327"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.7.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libssh2"] = None
        self.runtimeDependencies["libs/pcre2"] = None
        self.runtimeDependencies["libs/openssl"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()

        # ensure the more recent PCRE2 is used, per default it will pick up PCRE1 if found otherwise
        self.subinfo.options.configure.args += ["-DBUILD_CLAR=OFF", "-DREGEX_BACKEND=pcre2"]
