# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.2.6"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/project/libdc1394/libdc1394-2/{ver}/libdc1394-{ver}.tar.gz"
            self.archiveNames[ver] = f"libdc1394-{ver}.tar.gz"
            self.targetInstSrc[ver] = "libdc1394-" + ver
        self.description = "Provides API for IEEE 1394 cameras"
        self.defaultTarget = "2.2.6"
        # self.patchToApply['2.2.6'] = ("libdc1394-2.2.2-capture.patch", 1)

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libusb"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--disable-dependency-tracking", "--disable-examples", "--disable-sdltest"]
