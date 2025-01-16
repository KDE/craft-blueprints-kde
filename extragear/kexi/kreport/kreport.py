import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "A framework for the creation and generation of reports in multiple formats"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/python"] = None
        self.buildDependencies["dev-utils/system-python3"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None  # hard dependency for now
        self.runtimeDependencies["extragear/kexi/kproperty"] = None
        # TODO Windows/Mac: add marble libs (we only need marble widget), for now marble libs are disabled there
        if not CraftCore.compiler.isWindows and not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["kde/applications/marble"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DBUILD_EXAMPLES=ON"]
