# -*- coding: utf-8 -*-
import info
from Package.Qt5CorePackageBase import Qt5CorePackageBase
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        if CraftCore.compiler.isMinGW():
            self.patchToApply["5.15.2"] = [("0001-fix-wmf-plugin.patch", 1)]
            self.patchToApply["5.15.5"] = [("0001-fix-wmf-plugin.patch", 1)]
            self.patchToApply["kde/5.15"] = [("0001-fix-wmf-plugin.patch", 1)]
            self.patchToApply["kde/before-5.15.11-rebase"] = [("0001-fix-wmf-plugin.patch", 1)]
        self.patchLevel["5.15.2"] = 1
        self.patchLevel["kde/before-5.15.11-rebase"] = 1

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/pulseaudio"] = None


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.dynamic.featureArguments += ["-no-gstreamer", "-pulseaudio"]
