import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "A database connectivity and creation framework"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/python3"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/icu"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
