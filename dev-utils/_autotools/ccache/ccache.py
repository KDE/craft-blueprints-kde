# -*- coding: utf-8 -*-
import os
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/ccache/ccache.git"
        self.targetInstallPath["master"] = "dev-utils"

        for ver in ["4.6", "4.9"]:
            self.targets[ver] = f"https://github.com/ccache/ccache/releases/download/v{ver}/ccache-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ccache-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["4.6"] = (["73a1767ac6b7c0404a1a55f761a746d338e702883c7137fbf587023062258625"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.9"] = (["866b2223d59333640f0e7a003cbb85b32d9ca3c9445bd9e3cf142942e69dd3ec"], CraftHash.HashAlgorithm.SHA256)

        self.webpage = "https://ccache.dev/"
        self.defaultTarget = "4.9"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libzstd"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.supportsCCACHE = False
        self.subinfo.options.configure.args += ["-DREDIS_STORAGE_BACKEND=OFF"]

    def install(self):
        if not super().install():
            return False
        for t in [Path(os.environ["CXX"]), Path(os.environ["CC"])]:
            if not utils.createShim(
                self.installDir() / "ccache/bin" / t.name, self.installDir() / f"bin/ccache{CraftCore.compiler.executableSuffix}", args=[t]
            ):
                return False
        return True
