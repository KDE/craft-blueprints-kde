# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "A fast JSON parser/generator for C++ with both SAX/DOM style API"
        self.webpage = "https://rapidjson.org/"
        for ver in ["1.1.0"]:
            self.targets[ver] = f"https://github.com/Tencent/rapidjson/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"rapidjson-{ver}"

        self.svnTargets["24b5e7a"] = "https://github.com/Tencent/rapidjson.git||24b5e7a8b27f42fa16b96fc70aade9106cf7102f"

        self.svnTargets["master"] = "https://github.com/Tencent/rapidjson.git"

        self.defaultTarget = "24b5e7a"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DRAPIDJSON_BUILD_EXAMPLES=OFF"]
        if CraftCore.compiler.compiler.isGCCLike:
            self.subinfo.options.configure.args += ["-DCMAKE_CXX_FLAGS=-Wno-deprecated-declarations"]
