# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Open Source API and interchange format for editorial timeline information."
        self.webpage = "https://opentimeline.io"
        for ver in ["0.18.1"]:
            self.targets[ver] = f"https://github.com/AcademySoftwareFoundation/OpenTimelineIO/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"OpenTimelineIO-{ver}"

        self.targetDigests["0.18.1"] = (["bcb516a43a962dac0cde3e1f9da634c1fd409915d499ff8f3ce6f738a4637d72"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/AcademySoftwareFoundation/OpenTimelineIO.git"

        for ver in ["0.18.1"]:
            self.patchToApply[ver] = [("fix-windows-locations.patch", 1), ("fix-macos-rpath.patch", 1), ("1992.patch", 1)]
        self.patchLevel["0.18.1"] = 1

        self.defaultTarget = "0.18.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/imath"] = None
        self.runtimeDependencies["libs/rapidjson"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args += ["-DOTIO_FIND_IMATH=ON", "-DOTIO_FIND_RAPIDJSON=ON", "-DOTIO_DEPENDENCIES_INSTALL=OFF"]
