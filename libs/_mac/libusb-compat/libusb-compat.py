# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.1.5"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/project/libusb/libusb-compat-0.1/libusb-compat-{ver}/libusb-compat-{ver}.tar.bz2"
            self.archiveNames[ver] = "libusb-compat-%s.tar.bz2" % ver
            self.targetInstSrc[ver] = "libusb-compat-" + ver
        self.description = "Library for USB device access"
        self.defaultTarget = "0.1.5"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libusb"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += ["--disable-dependency-tracking"]
