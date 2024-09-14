# -*- coding: utf-8 -*-
# Copyright Filipe Azevedo <pasnox@gmail.com>
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
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/perl"] = None
        self.runtimeDependencies["perl-modules/xml-parser"] = None

    def setTargets(self):
        self.description = "Utility scripts for internationalizing XML."
        for ver in ["0.51.0"]:
            self.targets[ver] = f"https://launchpad.net/intltool/trunk/{ver}/+download/intltool-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"intltool-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.patchToApply["0.51.0"] = [("0001-Perl-5-22-compatibility.patch", 1)]
        self.targetDigests["0.51.0"] = (["67c74d94196b153b774ab9f89b2fa6c6ba79352407037c8c14d5aeb334e959cd"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["0.51.0"] = 1
        self.defaultTarget = "0.51.0"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        return self.patchInstallPrefix(
            [(self.imageDir() / x) for x in ["dev-utils/bin/intltoolize"]], self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot()
        )
