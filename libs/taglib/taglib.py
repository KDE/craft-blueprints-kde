import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.descriptions = "audio meta-data library"

    def setTargets(self):
        for ver in ["1.9.1", "1.11.1", "1.12", "1.13"]:
            self.targets[ver] = f"https://taglib.github.io/releases/taglib-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"taglib-{ver}"
            self.patchLevel[ver] = 1
        self.targetDigests["1.9.1"] = "4fa426c453297e62c1d1eff64a46e76ed8bebb45"
        self.targetDigests["1.11.1"] = (["b6d1a5a610aae6ff39d93de5efd0fdc787aa9e9dc1e7026fa4c961b26563526b"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.12"] = (["7fccd07669a523b07a15bd24c8da1bbb92206cb19e9366c3692af3d79253b703"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.13"] = (["58f08b4db3dc31ed152c04896ee9172d22052bc7ef12888028c01d8b1d60ade0"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.13"] = [("fix-mac-rpath.diff", 1)]
        self.patchLevel["1.13"] = 2
        self.description = "audio metadata library"
        self.webpage = "http://taglib.org/"
        self.defaultTarget = "1.13"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildStatic = False
        # self.subinfo.options.configure.args += ["-DBUILD_TESTS=ON", "-DBUILD_EXAMPLES=ON", "-DNO_ITUNES_HACKS=ON"]
        self.subinfo.options.configure.args += ["-DWITH_ASF=ON", "-DWITH_MP4=ON"]

    def postInstall(self):
        hardCoded = []
        if not CraftCore.compiler.isWindows:
            hardCoded += [(self.installDir() / x) for x in ["bin/taglib-config"]]
        return self.patchInstallPrefix(hardCoded, self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot())
