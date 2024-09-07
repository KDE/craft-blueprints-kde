import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["3.1.1"] = "https://github.com/openbabel/openbabel/archive/refs/tags/openbabel-3-1-1.tar.gz"
        self.targetInstSrc["3.1.1"] = "openbabel-openbabel-3-1-1"
        self.targetDigests["3.1.1"] = "22d5eea2492d4ea55fd29f9dcea34fd972af2a27"

        self.patchToApply["3.1.1"] = [
            ("0001-cmake-use-CMakePackageConfigHelpers-for-config-files.patch", 1),
            ("0001-Fix-CMake-config-install-location-on-Windows.patch", 1),
        ]

        self.description = "library to convert the various file formats used in chemical software"
        self.defaultTarget = "3.1.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/boost"] = None
        self.buildDependencies["libs/eigen3"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libxml2"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
