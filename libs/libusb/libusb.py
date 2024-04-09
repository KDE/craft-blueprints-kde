# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.24", "1.0.26"]:
            self.targets[ver] = f"https://github.com/libusb/libusb/releases/download/v{ver}/libusb-{ver}.tar.bz2"
            self.archiveNames[ver] = f"libusb-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libusb-{ver}"
        self.targetDigests["1.0.26"] = (["12ce7a61fc9854d1d2a1ffe095f7b5fac19ddba095c259e6067a46500381b5a5"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Library for USB device access"
        self.defaultTarget = "1.0.26"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        prefix = str(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))
        # self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += ["--disable-dependency-tracking", f"--prefix={prefix}"]
