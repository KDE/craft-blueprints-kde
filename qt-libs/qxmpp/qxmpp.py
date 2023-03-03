# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if self.options.isActive("libs/qt5/qtbase"):
            self.runtimeDependencies["libs/qt5/qtbase"] = None
            self.buildDependencies["libs/qt5/qttools"] = None
        else:
            self.runtimeDependencies["libs/qt6/qtbase"] = None
            self.buildDependencies["libs/qt6/qttools"] = None
            self.buildDependencies["libs/qt6/qt5compat"] = None

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/qxmpp-project/qxmpp.git'
        for ver in ["0.9.3", "1.0.0", "1.3.1", "1.3.2", "1.4.0"]:
            self.targets[ver] = f"https://github.com/qxmpp-project/qxmpp/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"qxmpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qxmpp-{ver}"
            self.patchToApply[ver] = [("0001-Install-dll-to-bindir-on-windows.patch", 1)]
        self.targetDigests['0.9.3'] = (
            ['13f5162a1df720702c6ae15a476a4cb8ea3e57d861a992c4de9147909765e6de'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.0.0'] = (
            ['bf62ac8d0b5741b3cb07ea92780b279d5c34d000dc7401d6c20a9b77865a5c1e'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.3.1'] = (
            ['812e718a2dd762ec501a9012a1281b9b6c6d46ec38adbc6eec242309144e1c55'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.3.2'] = (
            ['016e23c40c604dd43b15e1888e31d48729d0f80775fb6f7faef1130a52fe0641'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.4.0'] = (
            ['2148162138eaf4b431a6ee94104f87877b85a589da803dff9433c698b4cf4f19'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.4.0'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args = "-DBUILD_EXAMPLES=OFF -DBUILD_TESTS=OFF"
