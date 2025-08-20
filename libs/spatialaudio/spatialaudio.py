# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>


import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Ambisonic encoding / decoding and binauralization library in C++ "
        self.webpage = "https://github.com/videolabs/libspatialaudio"

        self.svnTargets["master"] = "https://github.com/videolabs/libspatialaudio.git"
        self.patchLevel["master"] = 20240907
        self.svnTargets["0b6b25e"] = "https://github.com/videolabs/libspatialaudio.git||0b6b25eba39fe1d2f4a981867957b9dcf62016db"
        self.defaultTarget = "0b6b25e"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [f"-DBUILD_STATIC_LIBS={self.subinfo.options.buildStatic.asOnOff}"]
