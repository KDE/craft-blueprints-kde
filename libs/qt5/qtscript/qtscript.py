# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None

        # kde patchcollection does not support qtscript anymore
        del self.svnTargets["kde/5.15"]
        del self.svnTargets["kde/before-5.15.11-rebase"]

        self.defaultTarget = "5.15.10"


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        super().__init__()
