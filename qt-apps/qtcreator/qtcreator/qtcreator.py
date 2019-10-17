# -*- coding: utf-8 -*-
import info
from Blueprints.CraftVersion import CraftVersion
from Blueprints.CraftPackageObject import CraftPackageObject

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://code.qt.io/qt-creator/qt-creator.git"
        
        for ver in ["4.10.1"]:
            majorVer = ".".join(ver.split(".")[:2])
            self.targets[ver] = f"http://download.qt.io/official_releases/qtcreator/{majorVer}/{ver}/qt-creator-opensource-src-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"qt-creator-opensource-src-{ver}"
            self.targetDigestUrls[ver] = f"https://download.qt.io/official_releases/qtcreator/{majorVer}/{ver}/qt-creator-opensource-src-{ver}.tar.xz.sha256"

        if CraftPackageObject.get("libs/llvm-meta/llvm").version == "9.0.0":
            self.patchToApply["4.10.1"] = [("qtcreator-4.10.1-20191017.diff", 1)]
        self.defaultTarget = "4.10.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtscript"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/llvm-meta/llvm"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["binary/python"] = None
        self.runtimeDependencies["dev-utils/clazy"] = None


from Package.CMakePackageBase import CMakePackageBase


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        # clangformat requires a patched clang
        self.subinfo.options.configure.args += " -DBUILD_PLUGIN_CLANGFORMAT=OFF -WITH_DOCS=ON"
