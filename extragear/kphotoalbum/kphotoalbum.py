# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/kphotoalbum.git"

        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["kde/kdegraphics/kipi-plugins"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
