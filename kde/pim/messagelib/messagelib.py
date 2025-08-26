import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        # QtWebEngine is a required dependency, but disabled on MinGW so we can't build this either
        # It is probably not a big deal because MSVC is used to build the PIM stack on Windows
        self.parent.package.categoryInfo.platforms = (
            CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMinGW() else CraftCore.compiler.Platforms.All
        )

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Messagelib library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None

        self.runtimeDependencies["kde/pim/kmime"] = None
        self.runtimeDependencies["kde/pim/akonadi"] = None
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = None
        self.runtimeDependencies["kde/pim/akonadi-mime"] = None
        self.runtimeDependencies["kde/pim/grantleetheme"] = None
        self.runtimeDependencies["kde/pim/kmailtransport"] = None
        self.runtimeDependencies["kde/pim/kmbox"] = None
        self.runtimeDependencies["kde/pim/pimcommon"] = None
        self.runtimeDependencies["kde/pim/libgravatar"] = None
        self.runtimeDependencies["kde/pim/libkleo"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ktexttemplate"] = None
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/qt/qtwebengine"] = None
        self.runtimeDependencies["kde/libs/ktextaddons"] = None
        self.runtimeDependencies["kde/pim/kidentitymanagement"] = None

        self.runtimeDependencies["libs/gpgme"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=OFF"]
