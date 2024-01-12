import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotMacOS
        if CraftCore.compiler.isMinGW():
            # ghostscript does not build
            self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NoPlatform

    def setTargets(self):
        """ """
        for ver in ["0.2.1", "0.2.6", "0.2.7", "0.2.8"]:
            self.targets[ver] = f"https://libspectre.freedesktop.org/releases/libspectre-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libspectre-{ver}"
        self.patchToApply["0.2.1"] = ("spectre-0.2.1-cmake.diff", 1)
        self.patchToApply["0.2.6"] = ("libspectre-0.2.6-20101117.diff", 1)
        if CraftCore.compiler.isWindows:
            self.patchToApply["0.2.7"] = [("libspectre-0.2.7-20131003.diff", 1), ("libspectre-new-ghostscript.diff", 1)]
            self.patchToApply["0.2.8"] = [("libspectre-0.2.7-20131003.diff", 1), ("libspectre-new-ghostscript.diff", 1)]
        self.targetDigests["0.2.6"] = "819475c7e34a1e9bc2e876110fee530b42aecabd"
        self.targetDigests["0.2.7"] = "a7efd97b82b84ff1bb7a0d88c7e35ad10cc84ea8"
        self.targetDigests["0.2.8"] = (["65256af389823bbc4ee4d25bfd1cc19023ffc29ae9f9677f2d200fa6e98bc7a8"], CraftHash.HashAlgorithm.SHA256)

        self.description = "a wrapper library for libgs"
        self.defaultTarget = "0.2.8"

    def setDependencies(self):
        self.runtimeDependencies["libs/ghostscript"] = None
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.isWindows:

    class Package(CMakePackageBase):
        def __init__(self, **args):
            super().__init__()

else:

    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            super().__init__()
            self.subinfo.options.useShadowBuild = False
            self.subinfo.options.configure.args += [" --disable-static", "--enable-shared"]
