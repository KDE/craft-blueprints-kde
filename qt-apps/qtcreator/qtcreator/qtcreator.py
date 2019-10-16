# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://code.qt.io/qt-creator/qt-creator.git"
        
        for ver in ["4.10.1"]:
            majorVer = ".".join(ver.split(".")[:2])
            self.targets[ver] = f"http://download.qt.io/official_releases/qtcreator/{majorVer}/{ver}/qt-creator-opensource-src-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"qt-creator-opensource-src-{ver}"
            self.targetDigestUrls[ver] = f"https://download.qt.io/official_releases/qtcreator/{majorVer}/{ver}/qt-creator-opensource-src-{ver}.tar.xz.sha256"
        self.defaultTarget = "4.10.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtscript"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/llvm-meta/llvm"] = None if self.buildTarget < CraftVersion("4.9") else "8.0"
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["binary/python"] = None
        self.runtimeDependencies["dev-utils/clazy"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        # clangformat requires a patched clang
        self.subinfo.options.configure.args += " -DBUILD_PLUGIN_CLANGFORMAT=OFF -WITH_DOCS=ON"
