# SPDX-FileCopyrightText: 2026 Melvin Keskin <melvo@olomono.de>
#
# SPDX-License-Identifier: CC0-1.0

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://gitlab.freedesktop.org/gstreamer/gstreamer.git"
        for ver in ["1.28.4"]:
            self.targets[ver] = f"https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"gstreamer-{ver}"
        self.targetDigests["1.28.4"] = (["f5adc7e8f448c10260b3b25aa101c9d540674c8d9a54c2b77a86d04f2b3b50dd"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.28.4"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.runtimeDependencies["libs/glib"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-Dexamples=disabled",
            f"-Dtests={self.subinfo.options.dynamic.buildTests.asEnabledDisabled}",
        ]
        self.subinfo.options.configure.ldflags += " -lintl"
