import info
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KLdap library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["libs/cyrus-sasl"] = None
        self.runtimeDependencies["libs/openldap"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]
        if CraftCore.compiler.platform.isMacOS:
            self.subinfo.options.configure.args += [
                f"-DLdap_INCLUDE_DIRS={CraftStandardDirs.craftRoot() / 'include'}",
                f"-DLdap_LIBRARY={CraftStandardDirs.craftRoot() / 'lib' / 'libldap.2.dylib'}",
                f"-DLber_LIBRARY={CraftStandardDirs.craftRoot() / 'lib' / 'liblber.2.dylib'}",
            ]
