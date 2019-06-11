import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        if CraftCore.compiler.isMSVC():
            self.patchToApply["5.55.0"] = [("kactivities-stats-5.55.0-20190320.diff", 1)]
            self.patchToApply["5.56.0"] = [("kactivities-stats-5.55.0-20190320.diff", 1)]
            self.patchToApply["5.57.0"] = [("kactivities-stats-5.55.0-20190320.diff", 1)]
            self.patchToApply["5.58.0"] = [("kactivities-stats-5.55.0-20190320.diff", 1)]
            self.patchToApply["5.59.0"] = [("kactivities-stats-5.55.0-20190320.diff", 1)]


        self.description = "A library for accessing the usage data collected by the activities system"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kactivities"] = None
        self.runtimeDependencies["libs/boost/boost-headers"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_TESTING=OFF "
