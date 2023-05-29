# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/amarok.git"

        ver = "2.9.0"
        self.defaultTarget = ver
        self.targets[ver] = "http://download.kde.org/download.php?url=stable/amarok/" + ver + "/src/amarok-" + ver + ".tar.bz2"
        self.targetInstSrc[ver] = "amarok-" + ver

    def setDependencies(self):
        self.runtimeDependencies["libs/taglib"] = None
        self.runtimeDependencies["libs/taglib-extras"] = None
        self.runtimeDependencies["qt-libs/phonon"] = None
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["binary/mysql"] = None
        self.runtimeDependencies["qt-libs/liblastfm"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.buildDependencies["libs/gettext"] = None
        self.description = "a powerful music player"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
