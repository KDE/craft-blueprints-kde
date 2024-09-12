import info
import utils
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["6.6.0"] = 1
        self.patchLevel["6.7.0"] = 1

    def setDependencies(self):
        self.buildDependencies["libs/qt6/qttools"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtshadertools"] = None
        self.runtimeDependencies["libs/qt6/qtsvg"] = None
        if not CraftCore.compiler.platform.isAndroid:
            self.runtimeDependencies["libs/qt6/qtlanguageserver"] = None


from Package.CMakePackageBase import *


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.platform.isWindows and self.buildType() == "Debug":
            # we use a shim pointing to the debug exe, therefor the debug infix is missing here
            self.subinfo.options.configure.args += ["-D_Python_EXECUTABLE_DEBUG=python3"]
