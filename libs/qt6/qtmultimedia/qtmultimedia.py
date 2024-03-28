import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        for ver in ["6.6.0", "6.6.1"]:
            self.patchToApply[ver] = [("qtmultimedia-android-suspend-crash-fix.diff", 1)]
        # TODO also needed in 6.7.0 once that exists!
        for ver in ["6.6.2", "6.6.3"]:
            self.patchToApply[ver] = [("change-551770-backport.diff", 1)]
        self.patchLevel["6.6.0"] = 4
        self.patchLevel["6.6.1"] = 1
        self.patchLevel["6.6.2"] = 1
        self.patchLevel["6.6.3"] = 1
        # TODO also needed in 6.7.0 once that exists!
        # self.patchLevel["6.7.0"] = 1

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtshadertools"] = None
        self.runtimeDependencies["libs/pulseaudio"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/ffmpeg"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += ["-DQT_FEATURE_pulseaudio=ON"]
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["-DQT_FEATURE_ffmpeg=OFF"]
