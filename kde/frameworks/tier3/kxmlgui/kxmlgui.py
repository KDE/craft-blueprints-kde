import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Framework for managing menu and toolbar actions"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None

        if CraftCore.compiler.isLinux or CraftCore.compiler.isFreeBSD:
            self.runtimeDependencies["kde/frameworks/tier3/kglobalaccel"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        if not CraftCore.compiler.isLinux and not CraftCore.compiler.isFreeBSD:
            self.subinfo.options.configure.args += "-DFORCE_DISABLE_KGLOBALACCEL=ON" # TODO only needed for KXmlGui < 5.82
