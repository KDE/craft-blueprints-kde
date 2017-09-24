# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/llvm-meta/clang"] = "default"

    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/clazy'
        self.svnTargets['1.2'] = 'git://anongit.kde.org/clazy|1.2'
        self.defaultTarget = '1.2'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsClang = False
        if craftCompiler.isMSVC():
            clangLib = os.path.join(CraftPackageObject.get('win32libs/llvm-meta/llvm').instance.buildDir(), "lib",
                                    "clang.lib")
            self.subinfo.options.configure.args = f"-DCLANG_LIBRARY_IMPORT='{clangLib}'"
