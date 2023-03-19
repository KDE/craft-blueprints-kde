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
        self.runtimeDependencies["libs/libomemo-c"] = None
        self.buildDependencies["libs/libomemo-c"] = None
        self.runtimeDependencies["kdesupport/qca"] = None

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/qxmpp-project/qxmpp.git'
        for ver in ["1.5.3"]:
            self.targets[ver] = f"https://github.com/qxmpp-project/qxmpp/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"qxmpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qxmpp-{ver}"
        self.targetDigests['1.5.3'] = (
            ['43ef503adcea8ef1a7eb0ce3af408eb693f66875550aaca9fd8309119e1afec8'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.5.3'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args = "-DBUILD_EXAMPLES=OFF -DBUILD_TESTS=OFF -DBUILD_OMEMO=ON"
