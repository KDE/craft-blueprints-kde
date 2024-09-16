# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import re

from Package.CMakePackageBase import CMakePackageBase


class Pattern(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DBUILD_WITH_QT6=ON", "-DQT_MAJOR_VERSION=6"]

    def createPackage(self):
        ver = self.getCMakeProjectVersion()
        if not ver:
            ver = self.getReleaseServiceVersion()

        if ver:
            self.defines["version"] = ver

        return super().createPackage()

    def getCMakeProjectVersion(self):
        cacheFile = self.buildDir() / "CMakeCache.txt"
        if not cacheFile.exists():
            return None

        with open(cacheFile) as f:
            for line in f:
                x = re.search(r"^CMAKE_PROJECT_VERSION\b.*=(.*)", line)
                if x:
                    return x.group(1)

        return None

    def getReleaseServiceVersion(self):
        cmakeFile = self.sourceDir() / "CMakeLists.txt"
        if not cmakeFile.exists():
            return None

        values = {}
        with open(cmakeFile) as f:
            for line in f:
                for var in ["RELEASE_SERVICE_VERSION_MAJOR", "RELEASE_SERVICE_VERSION_MINOR", "RELEASE_SERVICE_VERSION_MICRO"]:
                    regex = rf'set\s*\({var}\s+"(\d+)"\)'
                    x = re.search(regex, line)
                    if x:
                        values[var] = x.group(1)

        try:
            major = values["RELEASE_SERVICE_VERSION_MAJOR"]
            minor = values["RELEASE_SERVICE_VERSION_MINOR"]
            micro = values["RELEASE_SERVICE_VERSION_MICRO"]

            return f"{major}.{minor}.{micro}"
        except KeyError:
            return None
