# -*- coding: utf-8 -*-

import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.13", "4.16.0"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/libtasn1/libtasn1-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libtasn1-{ver}"
        self.targetDigests["4.13"] = (["7e528e8c317ddd156230c4e31d082cd13e7ddeb7a54824be82632209550c8cca"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.16.0"] = (["0e0fb0903839117cb6e3b56e68222771bebf22ad7fc2295a0ed7d576e8d4329d"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "4.16.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/gtk-doc"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # gtk-doc is missing
        self.subinfo.options.configure.autoreconf = not CraftCore.compiler.isWindows
