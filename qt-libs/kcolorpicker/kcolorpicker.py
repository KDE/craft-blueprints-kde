# SPDX-License-Identifier: GPL-2.0-only OR GPL-3.0-only OR LicenseRef-KDE-Accepted-GPL
# SPDX-FileCopyrightText: 2023 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/ksnip/kColorPicker.git"
        for ver in ["0.2.0"]:
            self.targets[ver] = f"https://github.com/ksnip/kColorPicker/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"kColorPicker-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kColorPicker-{ver}"
        self.targetDigests["0.2.0"] = (["20ffc5e935333a18c5cd813c3d306d3482ec9c826fe0d0c3d7b7635419703d55"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Qt based Color Picker with popup menu"
        self.defaultTarget = "0.2.0"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
