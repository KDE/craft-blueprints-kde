# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

import info
import utils
from Package.RustPackageBase import RustPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "GYP can Generate Your Projects."

        for ver in ["2.0.2"]:
            self.targets[ver] = f"https://github.com/gyroflow/gyroflow-plugins/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gyroflow-plugins-{ver}/frei0r"
        self.defaultTarget = "2.0.2"

    def setDependencies(self):
        self.buildDependencies["dev-utils/rust"] = None


class Package(RustPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        return utils.copyFile(self.buildDir() / "release/libgyroflow_frei0r.so", self.imageDir() / "lib/frei0r-1/libgyroflow_frei0r.so", linkOnly=False)
