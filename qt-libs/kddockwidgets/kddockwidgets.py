# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None

    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/KDAB/KDDockWidgets.git"
        for ver in ["1.2.0"]:
            self.targets[ver] = f"https://github.com/KDAB/KDDockWidgets/releases/download/v{ver}/kddockwidgets-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kddockwidgets-{ver}"
            self.archiveNames[ver] = f"kddockwidgets-{ver}.tar.gz"
        self.targetDigests["1.2.0"] = (
            ["b74657b6f2284c88917a239a522c63c7f06004c3915a9d5bf58c4a888251e3a3"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.2.0"

        self.description = "KDDockWidgets is a Qt dock widget library written by KDAB, suitable for replacing QDockWidget and implementing advanced functionalities missing in Qt."
        self.webpage = "https://www.kdab.com/introducing-kddockwidgets/"
        self.displayName = "KDDockWidgets"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
