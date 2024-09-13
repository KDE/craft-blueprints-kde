import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # Theoretically MSVC is supported, but with MSVC2022 there is an internal compiler error
        # MSVC 2019 seems to work, according to https://github.com/werman/noise-suppression-for-voice/commit/9c4e5c28d8950e2cef837d8a0abd36c2fd9b5c2d
        self.parent.package.categoryInfo.compiler &= CraftCore.compiler.Compiler.GCCLike

    def setTargets(self):
        self.description = "Real-time Noise Suppression Plugin"
        for ver in ["0.91", "1.03"]:
            self.targets[ver] = f"https://github.com/werman/noise-suppression-for-voice/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"noise-suppression-for-voice-{ver}"

        self.targetDigests["0.91"] = (["4f3a112534d4abb5ee2b6c328cde89193dbdb2146cffc98505972c3b5397a35e"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.03"] = (["8c85cae3ebbb3a18facc38930a3b67ca90e3ad609526a0018c71690de35baf04"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["0.91"] = [("0001-install-ladspa-in-lib.patch", 1)]
        self.patchToApply["1.03"] = [("0001-install-ladspa-in-lib.patch", 1)]

        self.svnTargets["master"] = "https://github.com/werman/noise-suppression-for-voice.git"

        # This commit breaks deploying the ladspa plugin on Windows, so stay at version 0.91 :
        # https://github.com/werman/noise-suppression-for-voice/commit/019673ed3bf0eedbd9b3f4d4f0a719d12fee5147
        if CraftCore.compiler.isMinGW():
            self.defaultTarget = "0.91"
            self.patchLevel["0.91"] = 1
        else:
            self.defaultTarget = "1.03"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DBUILD_VST_PLUGIN=OFF",
            "-DBUILD_VST3_PLUGIN=OFF",
            "-DBUILD_LV2_PLUGIN=OFF",
            "-DBUILD_AU_PLUGIN=OFF",
            "-DBUILD_AUV3_PLUGIN=OFF",
            f"-DBUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
        ]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir() / "lib", self.installDir() / "plugins")
        return True
