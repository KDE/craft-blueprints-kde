# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.24"]:
            self.targets[ver] = "https://github.com/libusb/libusb/releases/download/v" + ver + "/libusb-" + ver + ".tar.bz2"
            self.archiveNames[ver] = "libusb-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libusb-" + ver
        self.description = "Library for USB device access"
        self.defaultTarget = "1.0.24"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        prefix = str(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))
        # self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += " --disable-dependency-tracking" " --prefix=" + prefix
