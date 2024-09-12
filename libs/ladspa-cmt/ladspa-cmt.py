import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMSVC() else CraftCore.compiler.Platforms.All

    def setTargets(self):
        self.description = "The Computer Music Toolkit LADSPA plugin collection"
        self.webpage = "http://ladspa.org/"
        for ver in ["1.18"]:
            self.targets[ver] = "http://www.ladspa.org/download/cmt_" + ver + ".tgz"
            self.targetInstSrc[ver] = "cmt_" + ver + "/src"
            self.patchToApply[ver] = ("ladspa-cmt-cmake.patch", 0)
        self.targetDigests["1.18"] = (["a82f8636de1f4ada386a199a017a9cd775a49b49e716b11e8dd3f723c93df6ca"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.18"

    def setDependencies(self):
        self.buildDependencies["libs/ladspa-sdk"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.platform.isMacOS:
            return utils.mergeTree(self.installDir() / "lib", self.installDir() / "plugins")
        return True
