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
        ver = "24.08.0"
        self.targets[ver] = f"https://poppler.freedesktop.org/poppler-{ver}.tar.xz"
        self.targetInstSrc[ver] = f"poppler-{ver}"
        self.targetDigests[ver] = (["97453fbddf0c9a9eafa0ea45ac710d3d49bcf23a62e864585385d3c0b4403174"], CraftHash.HashAlgorithm.SHA256)
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
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/libcurl"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/fontconfig"] = None
        self.runtimeDependencies["data/poppler-data"] = None
        self.runtimeDependencies["data/urw-base35-fonts"] = None
        self.runtimeDependencies["libs/nss"] = None
        # Craft doesn't know how compile gpgme in Android
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/gpgme"] = None
        if self.options.dynamic.buildQtFrontend:
            self.runtimeDependencies["libs/qt/qtbase"] = None
        if self.options.dynamic.buildGlibFrontend:
            self.runtimeDependencies["libs/glib"] = None
            self.runtimeDependencies["libs/cairo"] = None

    def registerOptions(self):
        self.options.dynamic.registerOption("buildCppFrontend", not CraftCore.compiler.isAndroid)
        self.options.dynamic.registerOption("buildQtFrontend", True)
        self.options.dynamic.registerOption("buildGlibFrontend", False)
        self.options.dynamic.registerOption("buildUtils", False)
        if CraftCore.compiler.isAndroid:
            # Poppler doesn't support MinSizeRel
            self.options.dynamic.setDefault("buildType", "Release")


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # we use -DRUN_GPERF_IF_PRESENT=OFF to avoid running in gperf issues on windows during linking
        self.subinfo.options.configure.args += [
            "-DENABLE_XPDF_HEADERS=ON",
            "-DENABLE_UNSTABLE_API_ABI_HEADERS=ON",
            "-DENABLE_ZLIB=ON",
            "-DRUN_GPERF_IF_PRESENT=OFF",
        ]

        if not self.subinfo.options.dynamic.buildGlibFrontend:
            self.subinfo.options.configure.args += ["-DENABLE_GLIB=OFF"]
        if not self.subinfo.options.dynamic.buildUtils:
            self.subinfo.options.configure.args += ["-DENABLE_UTILS=OFF"]

        self.subinfo.options.configure.args += ["-DENABLE_QT5=OFF"]
        self.subinfo.options.configure.args += ["-DENABLE_QT6=ON"]

        if not self.subinfo.options.dynamic.buildTests:
            self.subinfo.options.configure.args += ["-DBUILD_QT5_TESTS=OFF", "-DBUILD_QT6_TESTS=OFF", "-DBUILD_CPP_TESTS=OFF", "-DBUILD_MANUAL_TESTS=OFF"]

        if not self.subinfo.options.isActive("libs/libjpeg-turbo"):
            self.subinfo.options.configure.args += ["-DENABLE_DCTDECODER=unmaintained"]
        if self.subinfo.options.isActive("libs/openjpeg"):
            self.subinfo.options.configure.args += ["-DENABLE_LIBOPENJPEG=openjpeg2"]
        else:
            self.subinfo.options.configure.args += ["-DENABLE_LIBOPENJPEG=unmaintained"]

        self.subinfo.options.configure.args += ["-DENABLE_LIBCURL=" + ("ON" if self.subinfo.options.isActive("libs/libcurl") else "OFF")]
        self.subinfo.options.configure.args += ["-DENABLE_CPP=" + ("ON" if self.subinfo.options.dynamic.buildCppFrontend else "OFF")]
        self.subinfo.options.configure.args += ["-DENABLE_LIBTIFF=" + ("ON" if self.subinfo.options.isActive("libs/tiff") else "OFF")]
        self.subinfo.options.configure.args += ["-DENABLE_LCMS=" + ("ON" if self.subinfo.options.isActive("libs/lcms2") else "OFF")]
        self.subinfo.options.configure.args += ["-DENABLE_BOOST=" + ("ON" if self.subinfo.options.isActive("libs/boost/boost-headers") else "OFF")]

        # Craft doesn't compile NSS and gpgme with mingw
        self.subinfo.options.configure.args += [
            "-DENABLE_NSS3=" + ("ON" if (self.subinfo.options.isActive("libs/nss") and not CraftCore.compiler.isMinGW()) else "OFF")
        ]
        self.subinfo.options.configure.args += [
            "-DENABLE_GPGME="
            + ("ON" if (self.subinfo.options.isActive("libs/gpgme") and not CraftCore.compiler.isMinGW() and not CraftCore.compiler.isAndroid) else "OFF")
        ]
