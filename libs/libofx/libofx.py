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
        self.targets['0.10.3'] = "https://downloads.sourceforge.net/project/libofx/libofx/libofx-0.10.3.tar.gz"
        self.targetDigests['0.10.3'] = (['7b5f21989afdd9cf63ab4a2df4ca398782f24fda2e2411f88188e00ab49e3069'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc['0.10.3'] = "libofx-0.10.3"

        if CraftCore.compiler.isMSVC():
            self.patchToApply['0.10.3'] = [("msvc.diff", 1)]                                        # https://github.com/libofx/libofx/pull/47
            self.patchToApply['0.10.3'] += [("getopt.diff", 1)]                                     # https://github.com/libofx/libofx/pull/50
            self.patchToApply['0.10.3'] += [("revert-correct-casting-of-iconv-inbuf-arg.patch", 1)] # https://github.com/libofx/libofx/issues/51

        self.description = "a parser and an API for the OFX (Open Financial eXchange) specification"
        self.defaultTarget = '0.10.3'
        self.patchLevel["0.10.3"] = 0

    def setDependencies(self):
        self.runtimeDependencies["libs/libopensp"] = None
        self.runtimeDependencies["libs/iconv"] = None


from Package.AutoToolsPackageBase import *

class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.shell.useMSVCCompatEnv = True
        openSPIncludeDir = OsUtils.toUnixPath(os.path.join(CraftStandardDirs.craftRoot(), "include/OpenSP"))
        openSPLibDir = OsUtils.toUnixPath(os.path.join(CraftStandardDirs.craftRoot(), "lib"))
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static", f"--with-opensp-includes={openSPIncludeDir}", f"--with-opensp-libs={openSPLibDir}"]

class Package(PackageAutotools):
    def __init__(self):
        PackageAutotools.__init__(self)

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMSVC():
            return utils.moveFile(self.installDir() / "lib/ofx.dll.lib", self.installDir() / "lib/ofx.lib")
        return True
