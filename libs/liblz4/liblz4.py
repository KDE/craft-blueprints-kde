import info
from Package.CMakePackageBase import *
from Package.MakeFilePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/lz4/lz4.git"
        for ver in ["1.9.2"]:
            self.targets[ver] = f"https://github.com/lz4/lz4/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"lz4-{ver}"
            self.archiveNames[ver] = f"lz4-{ver}.tar.gz"
            if CraftCore.compiler.isMSVC():
                self.targetConfigurePath[ver] = "contrib/cmake_unofficial"
        self.targetDigests["1.9.2"] = (["658ba6191fa44c92280d4aa2c271b0f4fbc0e34d249578dd05e50e76d0e5efcc"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Extremely Fast Compression algorithm"
        self.defaultTarget = "1.9.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.isMSVC():

    class Package(CMakePackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.dynamic.buildStatic = True

else:

    class Package(MakeFilePackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.useShadowBuild = False
            self.subinfo.options.make.supportsMultijob = False
            self.subinfo.options.make.args += f"liblz4.a"

        def make(self):
            # fix Makefile
            makefile = os.path.join(self.sourceDir(), "Makefile")
            with open(makefile, "rt") as f:
                content = f.read()

            content = content.replace(r"include Makefile.inc", r"#include Makefile.inc")

            with open(makefile, "wt") as f:
                f.write(content)
            return super().make()

        def install(self):
            utils.copyFile(os.path.join(self.sourceDir(), "lib", "liblz4.a"), os.path.join(self.imageDir(), "lib", "liblz4.a"))
            utils.copyFile(os.path.join(self.sourceDir(), "lib", "lz4.h"), os.path.join(self.imageDir(), "include", "lz4.h"))
            return True
