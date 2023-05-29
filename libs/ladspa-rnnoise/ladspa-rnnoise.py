import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Real-time Noise Suppression Plugin"
        # self.svnTargets["master"] = "https://github.com/werman/noise-suppression-for-voice"
        ver = "0.91"
        self.targets[ver] = f"https://github.com/werman/noise-suppression-for-voice/archive/refs/tags/v{ver}.tar.gz"
        self.targetInstSrc[ver] = f"noise-suppression-for-voice-{ver}"
        self.targetDigests[ver] = (["4f3a112534d4abb5ee2b6c328cde89193dbdb2146cffc98505972c3b5397a35e"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply[ver] = [("0001-install-ladspa-in-lib.patch", 1)]
        self.defaultTarget = "0.91"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DBUILD_VST_PLUGIN=OFF -DBUILD_LV2_PLUGIN=OFF "

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir() / "lib", self.installDir() / "plugins")
        return True
