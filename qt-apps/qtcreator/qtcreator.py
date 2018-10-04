# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "git://code.qt.io/qt-creator/qt-creator.git"
        for branch in ["4.3", "4.4", "4.5"]:
            self.svnTargets[branch] = f"git://code.qt.io/qt-creator/qt-creator.git|{branch}"

        for ver in ["4.7.1"]:
            majorVer = ".".join(ver.split(".")[:2])
            self.targets[ver] = f"http://download.qt.io/official_releases/qtcreator/{majorVer}/{ver}/qt-creator-opensource-src-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"qt-creator-opensource-src-{ver}"
        self.targetDigests['4.0.2'] = 'ef7c5760d7dc72cb68ee1ddf84cb4245e41c39d5'
        self.defaultTarget = "4.7.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtscript"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
