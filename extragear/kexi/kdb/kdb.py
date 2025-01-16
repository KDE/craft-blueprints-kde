import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "A database connectivity and creation framework"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/python"] = None
        self.buildDependencies["dev-utils/system-python3"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/icu"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
