# -*- coding: utf-8 -*-

import info
from Blueprints.CraftVersion import CraftVersion
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["qt-libs/phonon"] = None
        if CraftCore.compiler.isMSVC():
            self.runtimeDependencies["kdesupport/kdewin"] = None
        if OsUtils.isWin():
            self.runtimeDependencies["binary/vlc"] = None
        else:
            self.runtimeDependencies["libs/vlc"] = None

    def setTargets(self):
        for ver in ["0.12.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/phonon/phonon-backend-vlc/{ver}/phonon-backend-vlc-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/phonon/phonon-backend-vlc/{ver}/phonon-backend-vlc-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"phonon-backend-vlc-{ver}"

        self.svnTargets["master"] = "https://anongit.kde.org/phonon-vlc"

        self.description = "the vlc based phonon multimedia backend"
        self.defaultTarget = "0.12.0"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.subinfo.options.configure.args += ["-DQT_MAJOR_VERSION=6", "-DPHONON_BUILD_QT6=ON", "-DPHONON_BUILD_QT5=OFF"]
        else:
            self.subinfo.options.configure.args += ["-DPHONON_BUILD_QT5=ON", "-DPHONON_BUILD_QT6=OFF"]
