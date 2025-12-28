# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Jonah Brüchert <jbb@kaidan.im>

import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtlocation"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/maplibre/maplibre-native-qt|main"
        self.svnTargets["181f28b"] = "https://github.com/maplibre/maplibre-native-qt||181f28b8d147d10b9160e106694fbca811c911b9"
        self.defaultTarget = "181f28b"

        # See https://github.com/maplibre/maplibre-native-qt/pull/265
        self.patchToApply["master"] = [("265.patch", 1), ("lto-disable.patch", 1)]
        self.patchLevel["181f28b"] = 3


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.fetch.checkoutSubmodules = True

        self.subinfo.options.configure.args += [
            "-DMLN_WITH_OPENGL=ON", "-DMLN_WITH_VULKAN=OFF", "-DMLN_QT_WITH_WIDGETS=OFF"
        ]
