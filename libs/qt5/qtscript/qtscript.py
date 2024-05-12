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

        # https://github.com/macports/macports-ports/commit/37210501094e88965242db5aea61f7d3bdc1eed6
        self.patchToApply["5.15.13"] = [("patch-webkit-remove-wtf_ceil-workaround.diff", 0)]

        self.defaultTarget = "5.15.13"


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        super().__init__()
