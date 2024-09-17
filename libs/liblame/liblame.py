# -*- coding: utf-8 -*-
import info
import utils
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.MakeFilePackageBase import MakeFilePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.100"]:
            self.targets[ver] = f"https://sourceforge.net/projects/lame/files/lame/{ver}/lame-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"lame-{ver}"

        self.patchToApply["3.100"] = [("lame_init_old-missing-symfile.patch", 1), ("liblame-3.100-20190112.diff", 1)]
        self.targetDigests["3.100"] = (["ddfe36cab873794038ae2c1210557ad34857a4b6bdc515785d1da9e175b1da1e"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.100"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/nasm"] = None


if CraftCore.compiler.compiler.isGCCLike:

    class Package(AutoToolsPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.configure.args += ["--disable-gtktest", "--disable-frontend", "--enable-nasm"]

else:

    class Package(MakeFilePackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.useShadowBuild = False
            self.subinfo.options.make.supportsMultijob = False
            self.subinfo.options.make.args += f"-f Makefile.MSVC dll comp=msvc GTK=NO CRAFT_ARCH=x{CraftCore.compiler.architecture.bits}"
            if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
                self.subinfo.options.make.args += " MSVCVER=Win64 ASM=NO"
            else:
                self.subinfo.options.make.args += " ASM=YES"

        def configure(self, dummyDefines=""):
            return utils.copyFile(self.sourceDir() / "configMS.h", self.sourceDir() / "config.h", linkOnly=False)

        def install(self):
            return (
                utils.copyFile(self.sourceDir() / "include/lame.h", self.installDir() / "include/lame/lame.h", linkOnly=False)
                and utils.copyFile(self.sourceDir() / "output/lame_enc.dll", self.installDir() / "bin/lame_enc.dll", linkOnly=False)
                and utils.copyFile(self.sourceDir() / "output/lame_enc.lib", self.installDir() / "lib/lame_enc.lib", linkOnly=False)
                and utils.copyFile(self.sourceDir() / "output/libmp3lame.dll", self.installDir() / "bin/libmp3lame.dll", linkOnly=False)
                and utils.copyFile(self.sourceDir() / "output/libmp3lame.lib", self.installDir() / "lib/libmp3lame.lib", linkOnly=False)
            )
