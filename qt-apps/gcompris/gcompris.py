# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/gcompris"
        self.defaultTarget = "master"
        self.description = "GCompris is a high quality educational software suite comprising of numerous activities for children aged 2 to 10."

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args = "-DQt5_DIR=%s -DBUILD_STANDALONE=OFF" % CraftStandardDirs.craftRoot()
