# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftCore.compiler.isMacOS:
            self.options.dynamic.setDefault("buildTests", False)

    def setTargets(self):
        self.description = "Lilv is a C library to make the use of LV2 plugins as simple as possible for applications."
        self.webpage = "https://drobilla.net/software/lilv"

        self.svnTargets["master"] = "https://gitlab.com/lv2/lilv.git"
        self.patchLevel["master"] = 20250808

        for ver in ["0.24.24", "0.24.26"]:
            self.targets[ver] = f"https://download.drobilla.net/lilv-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"lilv-{ver}"
        self.targetDigests["0.24.24"] = (["6bb6be9f88504176d0642f12de809b2b9e2dc55621a68adb8c7edb99aefabb4f"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.24.26"] = (["22feed30bc0f952384a25c2f6f4b04e6d43836408798ed65a8a934c055d5d8ac"], CraftHash.HashAlgorithm.SHA256)

        self.patchLevel["0.24.24"] = 1

        self.defaultTarget = "0.24.26"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None
        self.runtimeDependencies["libs/zix"] = None
        self.runtimeDependencies["libs/serd"] = None
        self.runtimeDependencies["libs/sord"] = None
        self.runtimeDependencies["libs/lv2"] = None
        self.runtimeDependencies["libs/sratom"] = None

        if self.options.dynamic.buildTools:
            self.runtimeDependencies["libs/libsndfile"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if CraftCore.compiler.isWindows:
            # There are some relative symbolic links causing "ERROR: Dangerous symbolic link path was ignored"
            self.subinfo.options.unpack.sevenZipExtraArgs = ["-snld"]

        self.subinfo.options.configure.args += [
            "-Dbindings_py=disabled",
            f"-Dtools={self.subinfo.options.dynamic.buildTools.asEnabledDisabled}",
            f"-Dtests={self.subinfo.options.dynamic.buildTests.asEnabledDisabled}",
        ]
