# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotWindows
        self.options.dynamic.setDefault("buildType", "Release")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/llvm"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/sdk/clazy.git"
        self.targetUpdatedRepoUrl["master"] = (["https://anongit.kde.org/clazy"], "https://invent.kde.org/sdk/clazy.git")

        for ver in ["1.16"]:
            self.targets[ver] = f"https://download.kde.org/stable/clazy/{ver}/src/clazy-v{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/clazy/{ver}/src/clazy-v{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"clazy-v{ver}"
        self.patchToApply["1.16"] = [("0001-Don-t-require-gnu-coreutils-on-mac.patch", 1)]
        self.defaultTarget = "1.16"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.supportsClang = False
        if CraftCore.compiler.isMSVC():
            clangLib = CraftCore.standardDirs.craftRoot() / "lib/craft_clang_plugins.lib"
            self.subinfo.options.configure.args = f"-DCLANG_LIBRARY_IMPORT='{clangLib}'"
