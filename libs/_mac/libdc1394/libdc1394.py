# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.2.6"]:
            self.targets[ver] = "https://downloads.sourceforge.net/project/libdc1394/libdc1394-2/" + ver + "/libdc1394-" + ver + ".tar.gz"
            self.archiveNames[ver] = "libdc1394-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libdc1394-" + ver
        self.description = "Provides API for IEEE 1394 cameras"
        self.defaultTarget = "2.2.6"
        # self.patchToApply['2.2.6'] = ("libdc1394-2.2.2-capture.patch", 1)

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/_mac/libusb"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.useShadowBuild = False
        prefix = str(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--disable-dependency-tracking", "--disable-examples", "--disable-sdltest", f"--prefix={prefix}"]
