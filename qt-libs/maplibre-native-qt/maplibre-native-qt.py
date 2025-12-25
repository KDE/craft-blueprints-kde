# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/maplibre/maplibre-native-qt|main"
        self.defaultTarget = "master"

        # See https://github.com/maplibre/maplibre-native-qt/pull/265
        self.patchToApply["master"] = [("265.patch", 1)]


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            "-DMLN_WITH_OPENGL=ON", "-DMLN_WITH_VULKAN=OFF"
        ]
