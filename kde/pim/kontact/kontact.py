import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Kontact"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/pim/kpimtextedit"] = None
        self.runtimeDependencies["kde/pim/kontactinterface"] = None
        self.runtimeDependencies["kde/pim/libkdepim"] = None
        self.runtimeDependencies["kde/pim/grantleetheme"] = None
        self.runtimeDependencies["kde/pim/kdepim-runtime"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]
