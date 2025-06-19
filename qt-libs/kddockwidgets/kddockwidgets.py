# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None

    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/KDAB/KDDockWidgets.git"
        for ver in ["2.2.5"]:
            self.targets[ver] = f"https://github.com/KDAB/KDDockWidgets/releases/download/v{ver}/kddockwidgets-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kddockwidgets-{ver}"
            self.archiveNames[ver] = f"kddockwidgets-{ver}.tar.gz"
        self.targetDigests["2.2.5"] = (["1c202d03a0c7018aebcb249b09122d846b34298d88d0bc247a601f48c7513c89"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.2.5"

        self.description = "KDDockWidgets is a Qt dock widget library written by KDAB, suitable for replacing QDockWidget and implementing advanced functionalities missing in Qt."
        self.webpage = "https://www.kdab.com/introducing-kddockwidgets/"
        self.displayName = "KDDockWidgets"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DKDDockWidgets_QT6=ON", "-DKDDockWidgets_FRONTENDS=qtwidgets"]
