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
        for ver in ["2.1.1"]:
            self.targets[ver] = f"https://taglib.github.io/releases/taglib-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"taglib-{ver}"
        self.targetDigests["2.1.1"] = (["3716d31f7c83cbf17b67c8cf44dd82b2a2f17e6780472287a16823e70305ddba"], CraftHash.HashAlgorithm.SHA256)
        self.description = "audio metadata library"
        self.webpage = "http://taglib.org/"
        self.defaultTarget = "2.1.1"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.subinfo.options.configure.args += [f"-DBUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}", "-DBUILD_EXAMPLES=ON", "-DNO_ITUNES_HACKS=ON"]
        self.subinfo.options.configure.args += ["-DWITH_ASF=ON", "-DWITH_MP4=ON"]

    def postInstall(self):
        hardCoded = []
        if not CraftCore.compiler.isWindows:
            hardCoded += [(self.installDir() / x) for x in ["bin/taglib-config"]]
        return self.patchInstallPrefix(hardCoded, self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot())
