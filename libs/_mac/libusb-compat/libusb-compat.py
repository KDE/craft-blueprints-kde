# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.1.5"]:
            self.targets[ver] = "https://downloads.sourceforge.net/project/libusb/libusb-compat-0.1/libusb-compat-" + ver + "/libusb-compat-" + ver + ".tar.bz2"
            self.archiveNames[ver] = "libusb-compat-%s.tar.bz2" % ver
            self.targetInstSrc[ver] = "libusb-compat-" + ver
        self.description = "Library for USB device access"
        self.defaultTarget = "0.1.5"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libusb"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        prefix = str(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))
        # self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += ["--disable-dependency-tracking", f"--prefix={prefix}"]
