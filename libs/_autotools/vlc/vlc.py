# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.


import re

import CraftCore
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.0.19"]:
            self.targets[ver] = f"http://get.videolan.org/vlc/{ver}/vlc-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"vlc-{ver}"
        self.targetDigests["3.0.19"] = (["643e3294bafe922324663ca499515b7564f2794575fd7d2b7992d20896381745"], CraftHash.HashAlgorithm.SHA256)
        self.description = "VLC is a free and open source cross-platform multimedia player and framework that plays most multimedia files as well as DVDs, Audio CDs, VCDs, and various streaming protocols."
        self.defaultTarget = "3.0.19"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtx11extras"] = None
        self.runtimeDependencies["libs/dbus"] = None
        self.runtimeDependencies["libs/fontconfig"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/libarchive"] = None
        self.runtimeDependencies["libs/libogg"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/libssh2"] = None
        self.runtimeDependencies["libs/libvorbis"] = None
        self.runtimeDependencies["libs/taglib"] = None
        self.runtimeDependencies["libs/zlib"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += [
            "--disable-lua",
            "--disable-a52",
            "--enable-vpx=no",
            "--enable-sparkle=no",
            "--enable-harfbuzz=no",  # hb-ft.h missing in harfbuzz version that we ship at the time of this writing (2.7.2)
        ]
