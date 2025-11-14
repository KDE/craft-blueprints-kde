# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Potrace"
        self.description = "Transforming bitmaps into vector graphics"
        self.webpage = "https://potrace.sourceforge.net/"
        self.releaseManagerId = 3691

        for ver in ["1.16"]:
            self.targets[ver] = f"https://potrace.sourceforge.net/download/{ver}/potrace-{ver}.tar.gz"
            self.targetInstSrc[ver] = "potrace-" + ver

        self.patchToApply["1.16"] = [("potrace-1.16-add-cmake.diff", 1), ("potrace-1.16-fix-msvc.diff", 1)]
        self.patchLevel["1.16"] = 1

        self.defaultTarget = "1.16"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5"]
