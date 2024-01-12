# -*- coding: utf-8 -*-
from pathlib import Path

import info
from CraftSetupHelper import SetupHelper


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.12.0"] = [(".qt-5.12.0", 1)]
        self.patchToApply["5.15.2"] = [(".qt-5.15.2", 1)]
        self.patchToApply["5.15.5"] = [(".qt-5.15.5", 1)]
        self.patchToApply["kde/5.15"] = [(".qt-kde-5.15", 1)]
        self.patchToApply["kde/before-5.15.11-rebase"] = [(".qt-kde-5.15", 1)]
        self.patchLevel["5.15.2"] = 1
        self.patchLevel["kde/5.15"] = 1

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/d3dcompiler"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        super().__init__()
        if self.buildType() == "MinSizeRel":
            self.subinfo.options.dynamic.featureArguments += ["-no-feature-qml-debug"]

    def make(self):
        env = {}
        if CraftCore.compiler.isMinGW():
            # add the path to fxc to PATH
            fxc = CraftCore.cache.findApplication("fxc", forceCache=True)
            if not fxc:
                # import from an visual studio environment
                fxc = CraftCore.cache.findApplication("signtool", SetupHelper.getMSVCEnv()["PATH"], forceCache=True)
            env["PATH"] = os.environ["PATH"] + f":{Path(fxc).parent}"
        with utils.ScopedEnv(env):
            return super().make()
