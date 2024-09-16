# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "FreeRDP is a free remote desktop protocol library and clients"
        self.webpage = "http://www.freerdp.com/"
        for ver in ["2.11.7"]:
            self.targets[ver] = f"https://github.com/FreeRDP/FreeRDP/releases/download/{ver}/freerdp-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"freerdp-{ver}"
        self.targetDigests["2.11.7"] = (["5a2d54e1ca0f1facd1632bcc94c73b9f071a80c5fdbbb3f26e79f02aaa586ca3"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/FreeRDP/FreeRDP.git"
        self.defaultTarget = "2.11.7"

    def setDependencies(self):
        self.runtimeDependencies["libs/libusb"] = None
    #     self.runtimeDependencies["libs/zlib"] = None
    #     self.runtimeDependencies["libs/libsdl2"] = None
    #     self.runtimeDependencies["libs/opencv/opencv"] = None

class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.subinfo.options.dynamic.buildTests = False
        # self.subinfo.options.configure.args += ["-DWITH_EXAMPLES=OFF",
        #                                         "-DWITH_GTK=OFF",
        #                                         f"-DWITH_TESTS={'ON' if self.subinfo.options.dynamic.buildTests else 'OFF'}"]
