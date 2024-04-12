# -*- coding: utf-8 -*-

import info
from CraftStandardDirs import CraftStandardDirs
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/gcompris"
        self.defaultTarget = "master"
        self.description = "GCompris is a high quality educational software suite comprising of numerous activities for children aged 2 to 10."

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [f"-DQt5_DIR={CraftStandardDirs.craftRoot()}", "-DBUILD_STANDALONE=OFF"]
