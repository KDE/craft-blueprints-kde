import info
from Package.CMakePackageBase import CMakePackageBase
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["6.6.0"] = [("qtmultimedia-android-suspend-crash-fix.diff", 1)]
        self.patchToApply["6.6.0"] += [("qtmultimedia-mingw-fix.diff", 1)]
        self.patchLevel["6.6.0"] = 5

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
