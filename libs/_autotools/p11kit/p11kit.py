# -*- coding: utf-8 -*-

import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # it currently fails to link
        self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.NotWindows

    def setTargets(self):
        for ver in ["0.23.22", "0.24.0"]:
            self.targets[ver] = f"https://github.com/p11-glue/p11-kit/releases/download/{ver}/p11-kit-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"p11-kit-{ver}"
        self.targetDigests["0.24.0"] = (["81e6140584f635e4e956a1b93a32239acf3811ff5b2d3a5c6094e94e99d2c685"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.23.22"] = (["8a8f40153dd5a3f8e7c03e641f8db400133fb2a6a9ab2aee1b6d0cb0495ec6b6"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.24.0"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libtasn1"] = None
        self.runtimeDependencies["libs/libffi"] = None
        self.runtimeDependencies["libs/gettext"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--without-trust-paths"]
