# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.Qt5CorePackageBase import Qt5CorePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["kde/5.15"] = [("0002-fix-c++17-build.patch", 1)]
        if CraftCore.compiler.isMinGW():
            self.patchToApply["5.15.2"] = [("0001-fix-wmf-plugin.patch", 1)]
            self.patchToApply["5.15.5"] = [("0001-fix-wmf-plugin.patch", 1)]
            self.patchToApply["kde/5.15"] += [("0001-fix-wmf-plugin.patch", 1)]
            self.patchToApply["kde/before-5.15.11-rebase"] = [("0001-fix-wmf-plugin.patch", 1)]
        self.patchLevel["5.15.2"] = 1
        self.patchLevel["kde/before-5.15.11-rebase"] = 2

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/pulseaudio"] = None


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.dynamic.featureArguments += ["-no-gstreamer"]
        if CraftCore.compiler.isLinux:
            self.subinfo.options.dynamic.featureArguments += ["-pulseaudio"]
