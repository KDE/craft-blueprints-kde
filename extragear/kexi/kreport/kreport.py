import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "A framework for the creation and generation of reports in multiple formats"
        self.options.configure.args = " -DBUILD_EXAMPLES=ON"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/python3"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None  # hard dependency for now
        self.runtimeDependencies["extragear/kexi/kproperty"] = None
        # TODO Windows/Mac: add marble libs (we only need marble widget), for now marble libs are disabled there
        if not OsUtils.isWin() and not OsUtils.isMac():
            self.runtimeDependencies["kde/applications/marble"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
