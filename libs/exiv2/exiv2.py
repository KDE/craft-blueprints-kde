import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.27.5", "0.28.0"]:
            self.targets[ver] = f"https://github.com/Exiv2/exiv2/archive/refs/tags/v{ver}.tar.gz"
            self.archiveNames[ver] = f"v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"exiv2-{ver}"

        self.targetDigests["0.27.5"] = (["1da1721f84809e4d37b3f106adb18b70b1b0441c860746ce6812bb3df184ed6c"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.28.0"] = (["04c0675caf4338bb96cd09982f1246d588bcbfe8648c0f5a30b56c7c496f1a0b"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/Exiv2/exiv2.git"

        self.description = "an image metadata library"
        self.defaultTarget = "0.28.0"

    def setDependencies(self):
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/expat"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/brotli"] = None
        self.runtimeDependencies["libs/libcurl"] = None
        self.runtimeDependencies["libs/inih"] = None
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["-DEXIV2_BUILD_SAMPLES=OFF", "-DEXIV2_ENABLE_NLS=OFF", "-DIconv_IS_BUILT_IN=OFF"]
        if CraftCore.compiler.isWindows:
            self.subinfo.options.configure.args += ["-DICONV_ACCEPTS_CONST_INPUT=ON", "-DEXIV2_ENABLE_WIN_UNICODE=OFF"]
        else:
            self.subinfo.options.dynamic.buildStatic = False
