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
import utils
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash

if not CraftCore.compiler.isMSVC():

    class subinfo(info.infoclass):
        def setTargets(self):
            for ver in ["2.0.1"]:
                self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/gpgme/gpgme-{ver}.tar.bz2"
                self.targetInstSrc[ver] = f"gpgme-{ver}"

            self.targetDigests["2.0.1"] = (["821ab0695c842eab51752a81980c92b0410c7eadd04103f791d5d2a526784966"], CraftHash.HashAlgorithm.SHA256)

            self.defaultTarget = "2.0.1"

        def setDependencies(self):
            self.buildDependencies["dev-utils/msys"] = None
            self.runtimeDependencies["virtual/base"] = None
            self.runtimeDependencies["libs/gpg-error"] = None
            self.runtimeDependencies["libs/assuan2"] = None
            self.runtimeDependencies["libs/gnupg"] = None

    class Package(AutoToolsPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.configure.cflags += " -Wno-incompatible-pointer-types"
            self.subinfo.options.configure.args += ["--disable-gpg-test"]

        def install(self):
            if not super().install():
                return False
            if CraftCore.compiler.isWindows:
                return utils.mergeTree(self.installDir() / "libexec", self.installDir() / "bin")
            return True

else:

    class subinfo(info.infoclass):
        def setTargets(self):
            self.addCachedAutotoolsBuild(versionInfo="../../_msvc/version.ini")

        def setDependencies(self):
            self.runtimeDependencies["virtual/base"] = None
            self.runtimeDependencies["libs/mingw-crt4msvc"] = None
            self.runtimeDependencies["libs/assuan2"] = None
            self.runtimeDependencies["libs/gpg-error"] = None
            self.runtimeDependencies["libs/gnupg"] = None

    class Package(BinaryPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
