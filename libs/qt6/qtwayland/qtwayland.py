import info
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Linux | CraftCore.compiler.Platforms.FreeBSD

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["6.8.0"] = [("76e3c3d.diff", 1)]
        self.patchLevel["6.8.0"] = 1

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None


from Package.CMakePackageBase import *


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DQT_FEATURE_wayland_egl=ON"]
