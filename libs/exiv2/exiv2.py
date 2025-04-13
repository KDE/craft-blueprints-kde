import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.27.5", "0.28.5"]:
            self.targets[ver] = f"https://github.com/Exiv2/exiv2/archive/refs/tags/v{ver}.tar.gz"
            self.archiveNames[ver] = f"v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"exiv2-{ver}"

        self.targetDigests["0.27.5"] = (["1da1721f84809e4d37b3f106adb18b70b1b0441c860746ce6812bb3df184ed6c"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.28.5"] = (["e1671f744e379a87ba0c984617406fdf8c0ad0c594e5122f525b2fb7c28d394d"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/Exiv2/exiv2.git"

        self.description = "an image metadata library"
        self.defaultTarget = "0.28.5"

    def setDependencies(self):
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/expat"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/brotli"] = None
        self.runtimeDependencies["libs/libcurl"] = None
        if not CraftCore.compiler.isAndroid:
            # inih on Android uses versioned .so.0
            self.runtimeDependencies["libs/inih"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DEXIV2_BUILD_SAMPLES=OFF", "-DEXIV2_ENABLE_NLS=OFF", "-DIconv_IS_BUILT_IN=OFF"]
        if CraftCore.compiler.isWindows:
            self.subinfo.options.configure.args += ["-DICONV_ACCEPTS_CONST_INPUT=ON", "-DEXIV2_ENABLE_WIN_UNICODE=OFF"]
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["-DEXIV2_ENABLE_INIH=OFF", "-DEXIV2_BUILD_EXIV2_COMMAND=OFF"]
