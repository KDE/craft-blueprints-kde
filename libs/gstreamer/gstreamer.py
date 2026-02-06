# SPDX-FileCopyrightText: 2026 Melvin Keskin <melvo@olomono.de>
#
# SPDX-License-Identifier: CC0-1.0

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://gitlab.freedesktop.org/gstreamer/gstreamer.git"
        for ver in ["1.28.0"]:
            self.targets[ver] = f"https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"gstreamer-{ver}"
        self.targetDigests["1.28.0"] = (["6c8676bc39a2b41084fd4b21d2c37985c69ac979c03ce59575db945a3a623afd"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.28.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/bison"] = None
        self.runtimeDependencies["libs/glib"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-Dexamples=disabled",
            "-Dtests=disabled",
        ]
        self.subinfo.options.configure.ldflags += " -lintl"
