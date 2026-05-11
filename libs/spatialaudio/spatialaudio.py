# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>


import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Ambisonic encoding / decoding and binauralization library in C++ "
        self.webpage = "https://github.com/videolabs/libspatialaudio"

        for ver in ["0.4.0"]:
            self.targets[ver] = f"https://github.com/videolan/libspatialaudio/releases/download/{ver}/libspatialaudio-{ver}.tar.xz"
            self.targetInstSrc[ver] = "libspatialaudio-" + ver
        self.targetDigests["0.4.0"] = (["79f00d6f2695844764604897f704f4520440e1c9e63ccb2aff482717f66b6187"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.4.0"


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
