# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None

    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/KDAB/KDDockWidgets.git"
        for ver in ["2.3.0"]:
            self.targets[ver] = f"https://github.com/KDAB/KDDockWidgets/releases/download/v{ver}/kddockwidgets-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"KDDockWidgets-{ver}"
            self.archiveNames[ver] = f"KDDockWidgets-{ver}.tar.gz"
        self.targetDigests["2.3.0"] = (["843baf9e1812c1ab82fd81d85b57cbc0d29bb43245efeb2539039780004b1056"], CraftHash.HashAlgorithm.SHA256)
        self.svnTargets["1e25b35"] = "https://github.com/KDAB/KDDockWidgets.git||1e25b357bbc7e0485c172dde77c653fa30c26ba8"
        self.defaultTarget = "1e25b35"

        self.description = "KDDockWidgets is a Qt dock widget library written by KDAB, suitable for replacing QDockWidget and implementing advanced functionalities missing in Qt."
        self.webpage = "https://www.kdab.com/introducing-kddockwidgets/"
        self.displayName = "KDDockWidgets"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DKDDockWidgets_QT6=ON", "-DKDDockWidgets_FRONTENDS=qtwidgets"]
