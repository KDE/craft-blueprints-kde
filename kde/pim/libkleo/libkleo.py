import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        # gpgmepp is a required dependency, but disabled on MinGW so we can't build this either
        # It is probably not a big deal because MSVC is used to build the PIM stack on Windows
        self.parent.package.categoryInfo.platforms = (
            CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.compiler.isMinGW else CraftCore.compiler.Platforms.All()
        )

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Crypto library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["libs/gpgme/gpgme"] = None
        self.runtimeDependencies["libs/gpgme/gpgmepp"] = None
        self.runtimeDependencies["libs/boost"] = None
        self.runtimeDependencies["kde/libs/ktextaddons"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
