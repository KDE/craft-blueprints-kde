# -*- coding: utf-8 -*-
# Copyright 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>
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

import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        # Disable on MinGW as it is broken, needs someone to care
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMinGW() else CraftCore.compiler.Compiler.All

    def setTargets(self):
        self.targets["5.8.1"] = "https://www.aquamaniac.de/rdm/attachments/download/402/gwenhywfar-5.8.1.tar.gz"
        self.targetDigests["5.8.1"] = (["05397618b9cae0197a181835f67e19ba09652cf30e2c9d1fbb98f3f34dbf4e1f"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["5.8.1"] = "gwenhywfar-5.8.1"
        self.patchToApply["5.8.1"] = [("gwenhywfar-5.8.1-20211230.diff", 0)]
        if CraftCore.compiler.isMinGW():
            self.patchToApply["5.8.1"] += [("gwenhywfar-4.19.0-20180218.diff", 1)]
        self.patchLevel["5.8.1"] = 3

        self.targets["5.10.2"] = "https://www.aquamaniac.de/rdm/attachments/download/501/gwenhywfar-5.10.2.tar.gz"
        self.targetDigests["5.10.2"] = (["60a7da03542865501208f20e18de32b45a75e3f4aa8515ca622b391a2728a9e1"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["5.10.2"] = "gwenhywfar-5.10.2"
        self.patchToApply["5.10.2"] = [
            ("gwenhywfar-5.10.2-20231024.diff", 1)
        ]  # https://github.com/aqbanking/gwenhywfar/commit/0047982d2a2b83cdd3405732b84a3ee8788e0269
        self.patchLevel["5.10.2"] = 1
        self.defaultTarget = "5.10.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/xmlsec1"] = None
        self.runtimeDependencies["libs/gnutls"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


# 2018-02-11: compilation is successful if xmlmerge.exe gives any output in the console. For it to happen gnutls must be compiled with --enable-nls --enable-openssl-compatibility
class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--with-guis=qt5"]

        # For appImage builds the --enable-local-install is needed so that
        # the appImage is searched for gwenhywfar plugins
        if CraftCore.compiler.platform.isMacOS or CraftCore.compiler.platform.isLinux:
            self.subinfo.options.configure.args += ["--enable-local-install"]

        if CraftCore.compiler.platform.isLinux:
            self.subinfo.options.configure.args += ["--enable-binreloc"]

        # Disable autoreconf. Otherwise following errors prevent configuring:
        # configure.ac:618: warning: macro 'AM_PATH_LIBGCRYPT' not found in library
        # configure.ac:633: warning: macro 'AM_PATH_GPG_ERROR' not found in library
        self.subinfo.options.configure.autoreconf = False

        self.subinfo.options.configure.ldflags += " -lintl"
        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.autoreconf = True
            # it tires to locate qt but used native windows paths for -l
            # those are not supported by libtool
            self.subinfo.options.configure.ldflags += f" -lQt5Widgets -lQt5Gui -lQt5Core -lqtmain"

    def configure(self):
        if CraftCore.compiler.isMinGW():
            _, includedir = CraftCore.cache.getCommandOutput("qmake", "-query QT_INSTALL_HEADERS")
            includedir = self.shell.toNativePath(includedir.strip())
            widgetsdir = self.shell.toNativePath(os.path.join(includedir, "QtWidgets"))
            guidir = self.shell.toNativePath(os.path.join(includedir, "QtGui"))
            coredir = self.shell.toNativePath(os.path.join(includedir, "QtCore"))

            self.subinfo.options.configure.cxxflags += f"-I{widgetsdir} -I{guidir} -I{coredir} -I{includedir} "
        return super().configure()
