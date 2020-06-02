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
        self.description = "PDF rendering library based on xpdf-3.0"
        self.svnTargets["master"] = "git://git.freedesktop.org/git/poppler/poppler"

        for ver in ["0.85.0", "0.89.0"]:
            self.targets[ver] = f"https://poppler.freedesktop.org/poppler-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"poppler-{ver}"
        self.targetDigests["0.85.0"] = (['2bc875eb323002ae6b287e09980473518e2b2ed6b5b7d2e1089e36a6cd00d94b'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.89.0"] = (['fba230364537782cc5d43b08d693ef69c36586286349683c7b127156a8ef9b5c'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["0.85.0"] = [("poppler-0.85.0-20200602.diff", 1)]
        self.patchToApply["0.89.0"] = [("poppler-0.85.0-20200602.diff", 1)]
        self.defaultTarget = "0.89.0"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["data/poppler-data"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/lcms2"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/openjpeg"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/libcurl"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/fontconfig"] = None
        self.runtimeDependencies["data/poppler-data"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # we use -DRUN_GPERF_IF_PRESENT=OFF to avoid running in gperf issues on windows during linking
        self.subinfo.options.configure.args = "-DENABLE_XPDF_HEADERS=ON -DENABLE_ZLIB=ON -DENABLE_LIBCURL=ON -DENABLE_UTILS=OFF -DENABLE_LIBOPENJPEG=openjpeg2 -DENABLE_GLIB=OFF -DRUN_GPERF_IF_PRESENT=OFF"
