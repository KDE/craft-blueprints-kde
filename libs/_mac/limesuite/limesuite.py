# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["20.10.0"]:
            self.targets[ver] = f"https://github.com/myriadrf/LimeSuite/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"limesuite-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"LimeSuite-{ver}"
        self.description = "Lime suite device drivers, GUI, and SDR support"
        self.defaultTarget = "20.10.0"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["libs/swig"] = None
        self.buildDependencies["libs/libusb"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.useShadowBuild = False
        root = str(CraftCore.standardDirs.craftRoot())
        self.subinfo.options.configure.args += ["-DENABLE_STREAM=ON", "-DENABLE_GUI=OFF", "-DENABLE_NOVENARF7=OFF", "-DENABLE_SOAPY_LMS7=OFF", "-DLIME_SUITE_EXTVER=release", f"-DLIME_SUITE_ROOT={root}"]
