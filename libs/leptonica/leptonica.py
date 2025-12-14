# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Hennadii Chernyshchyk <genaloner@gmail.com>

import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.84.1"]:
            self.targets[ver] = f"https://github.com/DanBloomberg/leptonica/archive/{ver}/leptonica-{ver}.tar.gz"
            self.targetInstSrc[ver] = "leptonica-" + ver
            self.patchToApply[ver] = [("fix-pkgconfig-name.patch", 1)]
        self.targetDigests["1.84.1"] = "8e37f3f4486df65251d75e1f1c42e34b6b472694"

        self.description = "Software that is broadly useful for image processing and image analysis applications"
        self.webpage = "http://www.leptonica.com"
        self.defaultTarget = "1.84.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/giflib"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/webp"] = None
        self.runtimeDependencies["libs/openjpeg"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5", "-DSW_BUILD=OFF"]
