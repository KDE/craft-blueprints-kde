import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.5.21", "3.5.23", "3.5.25.3", "3.5.27", "3.5.30"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/djvu/djvulibre-{ver}.tar.gz"
            self.targetInstSrc[ver] = "djvulibre-" + ver
        self.targetInstSrc["3.5.25.3"] = "djvulibre-3.5.25"
        if CraftCore.compiler.platform.isWindows:
            self.patchToApply["3.5.21"] = [("djvu-cmake.diff", 0)]
            self.patchToApply["3.5.23"] = [("djvulibre-3.5.23-20101116.diff", 1)]
            self.patchToApply["3.5.25.3"] = [("djvulibre-3.5.25.3-20130906.diff", 1)]
            self.patchToApply["3.5.27"] = [("djvulibre-3.5.27-20151208.diff", 1), ("djvu-3.5.27-mingw.diff", 1)]
        self.targetDigests["3.5.23"] = (["608c07e629626cfe713168c942a07d2db3b0b19df4aae1f598473f4a2daf213d"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.5.25.3"] = (["898d7ed6dd2fa311a521baa95407a91b20a872d80c45e8245442d64f142cb1e0"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.5.27"] = (["e69668252565603875fb88500cde02bf93d12d48a3884e472696c896e81f505f"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.5.30"] = (["ee5e457d4cfebe566f94b99e5e3d3cc7f5c79ddb741c2ac2ba2e456f00329644"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "3.5.30"

        self.releaseManagerId = 10159
        self.webpage = "http://djvu.sourceforge.net/"
        self.description = "DjVuLibre is an implementation of DjVu image file format"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.platform.isMacOS:
            # attempting to build and install the png files will fail on macOS
            self.subinfo.options.configure.args += ["--disable-desktopfiles"]


class PackageCMake(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5", "-DBUILD_TOOLS=OFF"]


if CraftCore.compiler.platform.isWindows:

    class Package(PackageCMake):
        pass

else:

    class Package(PackageAutoTools):
        pass
