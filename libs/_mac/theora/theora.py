# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.1.1"]:
            self.targets[ver] = f"https://github.com/xiph/theora/archive/refs/tags/v{ver}.tar.gz"
            self.archiveNames[ver] = "libtheora-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "theora-" + ver
            self.targetDigests["1.1.1"] = (["1d5c3b25bbced448f3e741c42df6796e3d5e57136a74bcd68262318290ec2982"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Open video compression format"
        self.defaultTarget = "1.1.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libogg"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += ["--disable-dependency-tracking", "--disable-oggtest", "--disable-vorbistest", "--disable-examples"]
