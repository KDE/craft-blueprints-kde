import info
from Package.CMakePackageBase import CMakePackageBase
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtshadertools"] = None
        self.runtimeDependencies["libs/pulseaudio"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/ffmpeg"] = None

        self.patchLevel["6.6.0"] = 2


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += ["-DQT_FEATURE_pulseaudio=ON"]
