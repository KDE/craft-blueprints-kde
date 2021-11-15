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

        # always try to use latest libpoppler with all security fixes
        ver = "21.11.0"
        self.targets[ver] = f"https://poppler.freedesktop.org/poppler-{ver}.tar.xz"
        self.targetInstSrc[ver] = f"poppler-{ver}"
        self.targetDigests[ver] = (['31b76b5cac0a48612fdd154c02d9eca01fd38fb8eaa77c1196840ecdeb53a584'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply[ver] = [("poppler-optional-manual-tests.diff", 1)]
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["libs/boost/boost-headers"] = None
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
        self.subinfo.options.configure.args += "-DENABLE_XPDF_HEADERS=ON -DENABLE_UNSTABLE_API_ABI_HEADERS=ON -DENABLE_ZLIB=ON -DENABLE_UTILS=OFF -DENABLE_GLIB=OFF -DRUN_GPERF_IF_PRESENT=OFF"

        if not self.subinfo.options.dynamic.buildTests:
            self.subinfo.options.configure.args += " -DBUILD_QT5_TESTS=OFF -DBUILD_QT6_TESTS=OFF -DBUILD_CPP_TESTS=OFF -DBUILD_MANUAL_TESTS=OFF "

        if not self.subinfo.options.isActive("libs/libjpeg-turbo"):
            self.subinfo.options.configure.args += " -DENABLE_DCTDECODER=unmaintained"
        if self.subinfo.options.isActive("libs/openjpeg"):
            self.subinfo.options.configure.args += " -DENABLE_LIBOPENJPEG=openjpeg2"
        else:
            self.subinfo.options.configure.args += " -DENABLE_LIBOPENJPEG=unmaintained"
        if self.subinfo.options.isActive("libs/libcurl"):
            self.subinfo.options.configure.args += " -DENABLE_LIBCURL=ON"

        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += " -DWITH_NSS3=OFF -DENABLE_CPP=OFF"
