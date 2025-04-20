# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Hennadii Chernyshchyk <genaloner@gmail.com>

import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["5.4.1"]:
            self.targets[ver] = f"https://github.com/tesseract-ocr/tesseract/archive/{ver}/tesseract-{ver}.tar.gz"
            self.targetInstSrc[ver] = "tesseract-" + ver
        self.targetDigests["5.4.1"] = "e22bb217ab787fd89a26028391d8572028c8e7dd"

        self.description = "An OCR program"
        self.webpage = "https://github.com/tesseract-ocr/tesseract"
        self.patchLevel["5.4.1"] = 1
        self.defaultTarget = "5.4.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/leptonica"] = None
        self.runtimeDependencies["libs/libarchive"] = None
        self.runtimeDependencies["libs/libcurl"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DSW_BUILD=OFF", "-DBUILD_TRAINING_TOOLS=OFF"]
