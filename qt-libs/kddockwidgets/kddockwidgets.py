# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None

    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/KDAB/KDDockWidgets.git"
        for ver in ["1.5.0"]:
            self.targets[ver] = f"https://github.com/KDAB/KDDockWidgets/releases/download/v{ver}/kddockwidgets-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kddockwidgets-{ver}"
            self.archiveNames[ver] = f"kddockwidgets-{ver}.tar.gz"
        self.targetDigests["1.5.0"] = (["51df16d4118ef64b85c69d135f63783adec3e8e93ddf9970901b9f7f91fc34b9"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.5.0"

        self.description = "KDDockWidgets is a Qt dock widget library written by KDAB, suitable for replacing QDockWidget and implementing advanced functionalities missing in Qt."
        self.webpage = "https://www.kdab.com/introducing-kddockwidgets/"
        self.displayName = "KDDockWidgets"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
