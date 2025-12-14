import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.5.21", "3.5.23", "3.5.25.3", "3.5.27"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/djvu/djvulibre-{ver}.tar.gz"
            self.targetInstSrc[ver] = "djvulibre-" + ver
        self.targetInstSrc["3.5.25.3"] = "djvulibre-3.5.25"
        if CraftCore.compiler.isWindows:
            self.patchToApply["3.5.21"] = [("djvu-cmake.diff", 0)]
            self.patchToApply["3.5.23"] = [("djvulibre-3.5.23-20101116.diff", 1)]
            self.patchToApply["3.5.25.3"] = [("djvulibre-3.5.25.3-20130906.diff", 1)]
            self.patchToApply["3.5.27"] = [("djvulibre-3.5.27-20151208.diff", 1), ("djvu-3.5.27-mingw.diff", 1)]
        self.targetDigests["3.5.23"] = "b19f6b461515a52eb1048aec81e04dfd836d681f"
        self.targetDigests["3.5.25.3"] = "ad35056aabb1950f385360ff59520a82a6f779ec"
        self.targetDigests["3.5.27"] = "99c4f2c621c063bf8c8a1626030539fe5a8675f9"

        self.defaultTarget = "3.5.27"

        self.releaseManagerId = 10159
        self.webpage = "http://djvu.sourceforge.net/"
        self.description = "DjVuLibre is an implementation of DjVu image file format"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.isMacOS:
            # attempting to build and install the png files will fail on macOS
            self.subinfo.options.configure.args += ["--disable-desktopfiles"]


class PackageCMake(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5", "-DBUILD_TOOLS=OFF"]


if CraftCore.compiler.isWindows:

    class Package(PackageCMake):
        pass

else:

    class Package(PackageAutoTools):
        pass
