# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Potrace"
        self.description = "Transforming bitmaps into vector graphics"
        self.webpage = "https://potrace.sourceforge.net/"

        for ver in ["1.16"]:
            self.targets[ver] = f"https://potrace.sourceforge.net/download/{ver}/potrace-{ver}.tar.gz"
            self.targetInstSrc[ver] = "potrace-" + ver

        self.defaultTarget = "1.16"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--with-libpotrace"]
