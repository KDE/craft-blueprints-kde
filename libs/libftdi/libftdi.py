# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.4", "1.5"]:
            self.targets[ver] = f"https://www.intra2net.com/en/developer/libftdi/download/libftdi1-{ver}.tar.bz2"
            self.archiveNames[ver] = f"libftdi1-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libftdi1-{ver}"
        self.targetDigests["1.5"] = (["7c7091e9c86196148bd41177b4590dccb1510bfe6cea5bf7407ff194482eb049"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Library to talk to FTDI chips"
        self.defaultTarget = "1.5"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["libs/swig"] = None
        self.buildDependencies["libs/libusb"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DPYTHON_BINDINGS=OFF",
            "-DEXAMPLES=OFF",
            "-DFTDI_EEPROM=OFF",
            f"-DBUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
        ]
