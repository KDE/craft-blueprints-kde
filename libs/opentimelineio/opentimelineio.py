# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Open Source API and interchange format for editorial timeline information."
        self.webpage = "https://opentimeline.io"
        for ver in ["0.17.0"]:
            # self.targets[ver] = f"https://github.com/AcademySoftwareFoundation/OpenTimelineIO/archive/refs/tags/v{ver}.tar.gz"
            # self.targetInstSrc[ver] = f"OpenTimelineIO-{ver}"
            self.svnTargets[ver] = f"https://github.com/AcademySoftwareFoundation/OpenTimelineIO.git||v{ver}"

        self.svnTargets["6b9d292"] = "https://github.com/AcademySoftwareFoundation/OpenTimelineIO.git||6b9d292bf09159c4f20b2bdccfe3ad6a9300809f"

        self.svnTargets["master"] = "https://github.com/AcademySoftwareFoundation/OpenTimelineIO.git"

        for ver in ["0.17.0", "6b9d292"]:
            self.patchToApply[ver] = [("fix-windows-locations.patch", 1), ("fix-macos-rpath.patch", 1)]

        self.patchLevel["0.17.0"] = 5

        self.defaultTarget = "6b9d292"

    def setDependencies(self):
        self.runtimeDependencies["libs/imath"] = None
        self.runtimeDependencies["libs/rapidjson"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args += ["-DOTIO_FIND_IMATH=ON", "-DOTIO_FIND_RAPIDJSON=ON", "-DOTIO_DEPENDENCIES_INSTALL=OFF"]
