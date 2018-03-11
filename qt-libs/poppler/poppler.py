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

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "git://git.freedesktop.org/git/poppler/poppler"
        for ver in ["0.38.0", "0.57.0", "0.62.0"]:
            self.targets[ver] = f"http://poppler.freedesktop.org/poppler-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"poppler-{ver}"
        self.patchToApply["0.38.0"] = ("poppler-0.38.0-20151130.diff", 1)
        self.patchToApply["0.57.0"] = ("poppler-0.57.0-20170810.diff", 1)
        self.patchToApply["0.62.0"] = ("poppler-0.62.0-20180314.diff", 1)
        self.targetDigests["0.38.0"] = "62d334116e509d59cd1d8f172f02c0a81e73182f"
        self.targetDigests['0.57.0'] = (['0ea37de71b7db78212ebc79df59f99b66409a29c2eac4d882dae9f2397fe44d8'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['0.62.0'] = (['5b9a73dfd4d6f61d165ada1e4f0abd2d420494bf9d0b1c15d0db3f7b83a729c6'], CraftHash.HashAlgorithm.SHA256)

        self.description = "PDF rendering library based on xpdf-3.0"
        self.defaultTarget = "0.62.0"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = "default"
        self.runtimeDependencies["data/poppler-data"] = "default"
        self.runtimeDependencies["libs/freetype"] = "default"
        self.runtimeDependencies["libs/libjpeg-turbo"] = "default"
        self.runtimeDependencies["libs/lcms"] = "default"
        self.runtimeDependencies["libs/lcms2"] = "default"
        self.runtimeDependencies["libs/zlib"] = "default"
        self.runtimeDependencies["libs/openjpeg"] = "default"
        self.runtimeDependencies["libs/libjpeg-turbo"] = "default"
        self.runtimeDependencies["libs/libpng"] = "default"
        self.runtimeDependencies["libs/libcurl"] = "default"
        self.runtimeDependencies["libs/tiff"] = "default"
        self.runtimeDependencies["libs/win_iconv"] = "default"
        self.runtimeDependencies["data/poppler-data"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.package.packageName = "poppler"
        self.subinfo.options.configure.args = "-DENABLE_XPDF_HEADERS=ON -DENABLE_ZLIB=ON -DENABLE_LIBCURL=ON -DENABLE_UTILS=OFF -DENABLE_LIBOPENJPEG=openjpeg2"
