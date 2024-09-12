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

import re

import CraftCore
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.4.3"]:
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/gnupg/gnupg-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"gnupg-{ver}"

        self.targetDigests["2.4.3"] = (["a271ae6d732f6f4d80c258ad9ee88dd9c94c8fdc33c3e45328c4d7c126bd219d"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["2.4.3"] = [("fix-disabled-ldap.patch", 1)]
        self.patchLevel["2.4.3"] = 1

        self.defaultTarget = "2.4.3"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/assuan2"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.runtimeDependencies["libs/npth"] = None
        self.runtimeDependencies["libs/libksba"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/ntbtls"] = None
        if CraftCore.compiler.platform.isLinux:
            self.runtimeDependencies["libs/openldap"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--disable-doc"]

        if not CraftCore.compiler.platform.isLinux:
            self.subinfo.options.configure.args += ["--disable-ldap"]
