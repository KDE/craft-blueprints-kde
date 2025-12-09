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

import os

import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # Disable on MinGW as it is broken, needs someone to care
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMinGW() else CraftCore.compiler.Compiler.All

    def setTargets(self):
        self.targets["5.14.1"] = "https://www.aquamaniac.de/rdm/attachments/download/630/gwenhywfar-5.14.1.tar.gz"
        self.targetDigests["5.14.1"] = (["8916feaa99cb954f963f2cba8dd2dffe57cacf7f284daf00eab071aad6fe2ab3"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["5.14.1"] = "gwenhywfar-5.14.1"
        self.patchLevel["5.14.1"] = 1

        self.defaultTarget = "5.14.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gnutls"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


# 2018-02-11: compilation is successful if xmlmerge.exe gives any output in the console. For it to happen gnutls must be compiled with --enable-nls --enable-openssl-compatibility
class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--with-guis=qt6"]

        # For appImage builds the --enable-local-install is needed so that
        # the appImage is searched for gwenhywfar plugins
        if CraftCore.compiler.isMacOS or CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += ["--enable-local-install"]

        if CraftCore.compiler.isLinux:
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
            self.subinfo.options.configure.ldflags += " -lQt6Widgets -lQt6Gui -lQt6Core -lqtmain"

    def configure(self):
        if CraftCore.compiler.isMinGW():
            _, includedir = CraftCore.cache.getCommandOutput("qmake", "-query QT_INSTALL_HEADERS")
            includedir = self.shell.toNativePath(includedir.strip())
            widgetsdir = self.shell.toNativePath(os.path.join(includedir, "QtWidgets"))
            guidir = self.shell.toNativePath(os.path.join(includedir, "QtGui"))
            coredir = self.shell.toNativePath(os.path.join(includedir, "QtCore"))

            self.subinfo.options.configure.cxxflags += f"-I{widgetsdir} -I{guidir} -I{coredir} -I{includedir} "
        return super().configure()
