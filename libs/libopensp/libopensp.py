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


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.5.2"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/project/openjade/opensp/{ver}/OpenSP-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"OpenSP-{ver}"

        if CraftCore.compiler.isWindows:
            self.patchToApply["1.5.2"] = ("OpenSP-1.5.2-20110111.diff", 1)
        # elif CraftCore.compiler.compiler.isMinGW:
        #     self.patchToApply['1.5.2'] = ("OpenSP-1.5.2-20180505.diff", 1)
        self.targetDigests["1.5.2"] = "b4e903e980f8a8b3887396a24e067bef126e97d5"
        self.description = "a library for a SGML parser algorithm"
        self.defaultTarget = "1.5.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        # if CraftCore.compiler.compiler.isMinGW:
        #     self.buildDependencies["dev-utils/msys"] = None


class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--disable-doc-build"]

        if CraftCore.compiler.compiler.isMinGW:
            self.subinfo.options.configure.noDataRootDir = True

    def configure(self):
        if CraftCore.compiler.compiler.isMinGW:
            # to fix MessageReporter.cxx:126:49: error: cast from 'const OpenSP::MessageModule*' to 'long unsigned int' loses precision [-fpermissive]
            self.subinfo.options.configure.cxxflags += "-fpermissive "
        return super().configure()


if CraftCore.compiler.isMacOS or CraftCore.compiler.isLinux:

    class Package(PackageAutotools):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

else:

    class Package(CMakePackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
