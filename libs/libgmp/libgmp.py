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


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["6.1.2", "6.2.1"]:
            self.targets[ver] = f"https://gmplib.org/download/gmp/gmp-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"gmp-{ver}"
        self.targetDigests["6.1.2"] = (["5275bb04f4863a13516b2f39392ac5e272f5e1bb8057b18aec1c9b79d73d8fb2"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["6.2.1"] = (["eae9326beb4158c386e39a356818031bd28f3124cf915f8c5b1dc4c7a36b4d7c"], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.isMSVC():
            # https://github.com/microsoft/vcpkg/tree/64adda19c86e89526b5e27703a193c14477cce07/ports/gmp
            self.patchToApply["6.2.1"] = [(".msvc", 1)]
        self.defaultTarget = "6.2.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if CraftCore.compiler.isWindows:
            self.buildDependencies["dev-utils/msys"] = None
        if CraftCore.compiler.isMSVC():
            # with msvc clang.exe is used instead of yasm
            self.buildDependencies["libs/llvm"] = None


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell.useMSVCCompatEnv = True
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--enable-cxx", "--with-pic", "--with-readline=no"]
        if CraftCore.compiler.isMSVC():
            # https://github.com/microsoft/vcpkg/tree/64adda19c86e89526b5e27703a193c14477cce07/ports/gmp
            self.subinfo.options.configure.args += [
                "ASMFLAGS=-c --target=x86_64-pc-windows-msvc",
                "CCAS=clang",
                "ac_cv_func_memset=yes",
                "gmp_cv_asm_w32=.word",
            ]
        self.subinfo.options.useShadowBuild = False


class Package(PackageAutoTools):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
