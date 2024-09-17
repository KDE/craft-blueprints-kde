# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.MSBuildPackageBase import MSBuildPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.27"]:
            self.targets[ver] = f"https://github.com/libusb/libusb/releases/download/v{ver}/libusb-{ver}.tar.bz2"
            self.archiveNames[ver] = f"libusb-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libusb-{ver}"
        self.targetDigests["1.0.27"] = (["ffaa41d741a8a3bee244ac8e54a72ea05bf2879663c098c82fc5757853441575"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Library for USB device access"
        self.defaultTarget = "1.0.27"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.isMSVC():

    class Package(MSBuildPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.configure.projectFile = self.sourceDir() / "msvc/libusb.sln"

else:

    class Package(AutoToolsPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # self.subinfo.options.useShadowBuild = False
            # self.subinfo.options.configure.args += ["--disable-dependency-tracking"]
