import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        if not CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            # Removed in KDE Frameworks 6
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler
        elif CraftCore.compiler.isMacOS:
            # Same as QtWebKit as it has a hard requirement on that
            self.parent.package.categoryInfo.architecture = CraftCore.compiler.Architecture.x86_64

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in self.targets:
            self.targets[ver] = self.versionInfo.format(
                "https://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/${PACKAGE_NAME}-${VERSION}.tar.xz", ver
            )
            self.targetDigestUrls[ver] = self.versionInfo.format(
                "https://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/${PACKAGE_NAME}-${VERSION}.tar.xz.sha256", ver
            )

        self.description = "KDE Integration for QtWebKit"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtwebkit"] = (None, info.DependencyRequirementType.Required)
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
