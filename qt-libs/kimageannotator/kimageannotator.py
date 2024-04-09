# SPDX-License-Identifier: GPL-2.0-only OR GPL-3.0-only OR LicenseRef-KDE-Accepted-GPL
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/ksnip/kImageAnnotator.git"
        for ver in ["0.6.0"]:
            self.targets[ver] = f"https://github.com/ksnip/kImageAnnotator/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"kImageAnnotator-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kImageAnnotator-{ver}"
        self.targetDigests["0.6.0"] = (["148ef703ed5535a0c23d11629b588d9cb163598798261aa760d5b351756646a7"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Tool for annotating images"
        self.defaultTarget = "0.6.0"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["qt-libs/kcolorpicker"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
