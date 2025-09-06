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

import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildStatic", not CraftCore.compiler.compiler.isMinGW)

    def setTargets(self):
        self.targets["1.3.0"] = "https://github.com/yasm/yasm/archive/v1.3.0.tar.gz"
        self.archiveNames["1.3.0"] = "yasm-1.3.0.tar.gz"
        self.targetDigests["1.3.0"] = (["f708be0b7b8c59bc1dbe7134153cd2f31faeebaa8eec48676c10f972a1f13df3"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["1.3.0"] = "yasm-1.3.0"
        self.targetInstallPath["1.3.0"] = "dev-utils"
        self.patchToApply["1.3.0"] = [("yasm-1.3.0-20190723.diff", 1), ("yasm-Fix-build-with-autotools-2.70.patch", 1)]
        self.patchLevel["1.3.0"] = 2

        self.description = "The Yasm Modular Assembler Project"
        self.defaultTarget = "1.3.0"

    def setDependencies(self):
        if CraftCore.compiler.platform.isUnix:
            self.buildDependencies["libs/gettext"] = None
            self.buildDependencies["libs/iconv"] = None
            self.buildDependencies["dev-utils/intltool"] = None
            self.buildDependencies["dev-utils/cmake"] = None

        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.compiler.isMinGW:

    class Package(AutoToolsPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.configure.autoreconfArgs += " -I m4"

else:

    class Package(CMakePackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
