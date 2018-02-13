# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/llvm-meta/clang"] = "default"

    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/clazy'
        for ver in ["1.3"]:
            self.targets[ver] = f"https://download.kde.org/stable/clazy/{ver}/src/clazy-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"clazy-{ver}"
        self.defaultTarget = '1.3'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsClang = False
        if CraftCore.compiler.isMSVC():
            clangLib = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "clang.lib")
            self.subinfo.options.configure.args = f"-DCLANG_LIBRARY_IMPORT='{clangLib}'"
