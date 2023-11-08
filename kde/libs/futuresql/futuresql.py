# SPDX-FileCopyrightText: 2023 Nicolas Fella <nicolas.fella@gmx.de>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/futuresql.git"

        for ver in ["0.1.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/futuresql/futuresql-{ver}.tar.xz"
            self.archiveNames[ver] = f"futuresql-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"futuresql-{ver}"

        self.description = "A non-blocking database framework for Qt."
        self.defaultTarget = "0.1.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["-DBUILD_EXAMPLES=OFF"]
