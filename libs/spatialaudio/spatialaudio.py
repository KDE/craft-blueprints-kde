# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>


import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Ambisonic encoding / decoding and binauralization library in C++ "
        self.webpage = "https://github.com/videolabs/libspatialaudio"

        for ver in ["0.3.0", "0.4.0"]:
            self.targets[ver] = f"https://github.com/videolan/libspatialaudio/releases/download/{ver}/libspatialaudio-{ver}.tar.xz"
            self.targetInstSrc[ver] = "libspatialaudio-" + ver
        self.targetDigests["0.4.0"] = (["79f00d6f2695844764604897f704f4520440e1c9e63ccb2aff482717f66b6187"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.4.0"] = (["79f00d6f2695844764604897f704f4520440e1c9e63ccb2aff482717f66b6187"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/videolabs/libspatialaudio.git"
        self.patchLevel["master"] = 20240907

        self.svnTargets["0b6b25e"] = "https://github.com/videolabs/libspatialaudio.git||0b6b25eba39fe1d2f4a981867957b9dcf62016db"
        # https://github.com/videolan/libspatialaudio/pull/91
        self.patchToApply["0b6b25e"] = [("fix-pkgconfig-file-msvc.patch", 1)]
        self.patchLevel["0b6b25e"] = 1

        self.svnTargets["5dda58e"] = "https://github.com/videolabs/libspatialaudio.git||5dda58ee0bee3ec808d01b044dcf7392b7d30c3d"

        # Version 0.4.0 contains breaking changes and MLT is not yet compatible with it
        self.defaultTarget = "0b6b25e"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
            f"-DBUILD_STATIC_LIBS={self.subinfo.options.buildStatic.asOnOff}",
            # TODO: exporting all symbols is no ideal, it should be fixed
            # upstream by using cmake's GenerateExportHeader etc.
            "-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=ON",
        ]
