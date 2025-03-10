# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

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

        self.svnTargets["master"] = "https://github.com/AcademySoftwareFoundation/OpenTimelineIO.git"
        # self.patchLevel["b7bc13a"] = 4
        # self.patchToApply["b7bc13a"] = [("pi_patch.diff", 1)]

        self.defaultTarget = "0.17.0"

    def setDependencies(self):
        self.runtimeDependencies["libs/imath"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args += ["-DOTIO_FIND_IMATH=ON", "-DOTIO_DEPENDENCIES_INSTALL=OFF"]
