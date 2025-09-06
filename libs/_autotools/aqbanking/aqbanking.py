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
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # Disable on MinGW as gwenhywfar is broken but apparently a mandatory dep, needs someone to care
        self.parent.package.categoryInfo.platforms = (
            CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.compiler.isMinGW else CraftCore.compiler.Compiler.All()
        )

    def setTargets(self):
        self.targets["6.5.4"] = "https://www.aquamaniac.de/rdm/attachments/download/499/aqbanking-6.5.4.tar.gz"
        self.targetDigests["6.5.4"] = (["0d16ceae76f0718e466638f4547a8b14927f1d8d98322079cd6481adde30ac99"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["6.5.4"] = "aqbanking-6.5.4"

        self.targets["6.6.1"] = "https://www.aquamaniac.de/rdm/attachments/download/535/aqbanking-6.6.1.tar.gz"
        self.targetDigests["6.6.1"] = (["3250fa6d893f816d29c19af35fe5fccb74c080e21753fd9e52579a792dd48567"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["6.6.1"] = "aqbanking-6.6.1"
        self.defaultTarget = "6.6.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/xmlsec1"] = None
        self.runtimeDependencies["libs/gwenhywfar"] = None
        if CraftCore.compiler.compiler.isMinGW:
            self.buildDependencies["dev-utils/msys"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # For appImage builds the --enable-local-install is needed so that
        # the appImage is searched for aqbanking plugins
        if CraftCore.compiler.platform.isMacOS or CraftCore.compiler.platform.isLinux:
            self.subinfo.options.configure.args += ["--enable-local-install"]

        if not self.subinfo.options.isActive("libs/gwenhywfar"):
            self.subinfo.options.configure.args += ["--enable-gwenhywfar=no"]

        # this prevents "cannot find the library libaqhbci.la or unhandled argument libaqhbci.la"
        self.subinfo.options.make.supportsMultijob = False

        # Including libtool from the newer autotools in craftroot breaks the build (at least on macOS)
        self.subinfo.options.configure.autoreconf = False

    def postInstall(self):
        cmakes = [self.installDir() / f"lib/cmake/aqbanking-{self.subinfo.buildTarget[:-2]}/aqbanking-config.cmake"]
        for cmake in cmakes:
            with open(cmake, "rt") as f:
                cmakeFileContents = f.readlines()
            for i in range(len(cmakeFileContents)):
                if CraftCore.compiler.compiler.isMinGW:
                    m = re.search(r'set_and_check\(prefix "(?P<root>[^"]*)"\)', cmakeFileContents[i])
                    if m is not None:
                        craftRoot = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
                        if craftRoot.endswith("/"):
                            craftRoot = craftRoot[:-1]
                        cmakeFileContents[i] = cmakeFileContents[i].replace(m.group("root"), craftRoot)
                elif CraftCore.compiler.platform.isMacOS:
                    m2 = re.search(r"(libaqbanking.so.(\d*))", cmakeFileContents[i])
                    if m2 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace(m2.group(1), f"libaqbanking.{m2.group(2)}.dylib")
            with open(cmake, "wt") as f:
                f.write("".join(cmakeFileContents))
        return super().postInstall()
