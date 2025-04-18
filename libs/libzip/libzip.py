# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.8.0", "1.11.3"]:
            self.targets[ver] = f"https://github.com/nih-at/libzip/releases/download/v{ver}/libzip-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libzip-{ver}"
        self.targetDigests["1.8.0"] = (["30ee55868c0a698d3c600492f2bea4eb62c53849bcf696d21af5eb65f3f3839e"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.11.3"] = (["76653f135dde3036036c500e11861648ffbf9e1fc5b233ff473c60897d9db0ea"], CraftHash.HashAlgorithm.SHA256)

        self.description = "a library for handling zip archives"
        self.defaultTarget = "1.11.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/libzstd"] = None
        self.runtimeDependencies["libs/nettle"] = None
        self.runtimeDependencies["libs/gnutls"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
