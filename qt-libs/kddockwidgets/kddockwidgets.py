# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None

    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/KDAB/KDDockWidgets.git"
        for ver in ["2.4.0"]:
            self.targets[ver] = f"https://github.com/KDAB/KDDockWidgets/releases/download/v{ver}/kddockwidgets-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"KDDockWidgets-{ver}"
            self.archiveNames[ver] = f"KDDockWidgets-{ver}.tar.gz"
        self.targetDigests["2.4.0"] = (["51dbf24fe72e43dd7cb9a289d3cab47112010f1a2ed69b6fc8ac0dff31991ed2"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.4.0"

        self.patchToApply["2.4.0"] = [("qtabbar_style.diff", 1)]
        self.patchLevel["2.4.0"] = 2

        self.description = "KDDockWidgets is a Qt dock widget library written by KDAB, suitable for replacing QDockWidget and implementing advanced functionalities missing in Qt."
        self.webpage = "https://www.kdab.com/introducing-kddockwidgets/"
        self.displayName = "KDDockWidgets"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DKDDockWidgets_QT6=ON", "-DKDDockWidgets_FRONTENDS=qtwidgets"]
