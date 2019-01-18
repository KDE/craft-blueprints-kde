# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "git://code.qt.io/qt-creator/qt-creator.git"
        for branch in ["4.3", "4.4", "4.5"]:
            self.svnTargets[branch] = f"git://code.qt.io/qt-creator/qt-creator.git|{branch}"

        for ver in ["4.7.1", "4.8.0", "4.8.1"]:
            majorVer = ".".join(ver.split(".")[:2])
            self.targets[ver] = f"http://download.qt.io/official_releases/qtcreator/{majorVer}/{ver}/qt-creator-opensource-src-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"qt-creator-opensource-src-{ver}"
            self.targetDigestUrls[ver] = f"https://download.qt.io/official_releases/qtcreator/{majorVer}/{ver}/qt-creator-opensource-src-{ver}.tar.xz.sha256"
        self.patchLevel["4.7.1"] = 1
        self.defaultTarget = "4.8.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtscript"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/llvm-meta/llvm"] = None
        self.runtimeDependencies["binary/python"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
        self.subinfo.options.install.args = "install install_docs"
        self._buildEnv = {}
        if CraftCore.compiler.isWindows:
            self._buildEnv = {"PYTHON_INSTALL_DIR":CraftCore.settings.get("Paths", "Python")}

    def configure(self, configureDefines=""):
        with utils.ScopedEnv(self._buildEnv):
            return super().configure(configureDefines)

    def make(self):
        with utils.ScopedEnv(self._buildEnv):
            if not super().make():
                return False
            return utils.system(f"{self.makeProgram} {self.makeOptions('docs')}")
