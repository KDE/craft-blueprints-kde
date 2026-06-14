import info
from Blueprints.CraftVersion import CraftVersion
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "mbox library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if self.buildTarget == "master" or CraftVersion(self.buildTarget) > CraftVersion("26.04.3"):
            self.runtimeDependencies["kde/frameworks/tier2/kmime"] = None
        else:
            self.runtimeDependencies["kde/pim/kmime"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]
