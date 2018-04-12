# -*- coding: utf-8 -*-
# Copyright Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>
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
        self.targets['0.9.12'] = "http://downloads.sourceforge.net/project/libofx/libofx/libofx-0.9.12.tar.gz"
        self.targetDigests['0.9.12'] = (['c15fa062fa11e759eb6d8c7842191db2185ee1b221a3f75e9650e2849d7b7373'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc['0.9.12'] = "libofx-0.9.12"
        self.patchToApply['0.9.12'] = [("libofx-0.9.5-20120131.diff", 1)]
        self.patchToApply['0.9.12'] += [("libofx-0.9.12-20180127.diff", 1)]

        if CraftCore.compiler.isMSVC():
            self.patchToApply['0.9.12'] += [("patch_daylight.diff", 1)]
        if CraftCore.compiler.isMinGW():
            self.patchToApply['0.9.12'] += [("libofx-0.9.12-20180127-mingw.diff", 1)]

        self.patchToApply['0.9.12'] += [("libofx-0.9.12-20180412.diff", 1)]

        self.description = "a parser and an API for the OFX (Open Financial eXchange) specification"
        self.defaultTarget = '0.9.12'

    def setDependencies(self):
        self.runtimeDependencies["libs/libopensp"] = "default"
        self.runtimeDependencies["libs/iconv"] = "default"


from Package.AutoToolsPackageBase import *
from Package.CMakePackageBase import *

class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        openSPIncludeDir = CraftStandardDirs.craftRoot() + "/include/OpenSP"
        openSPLibDir = CraftStandardDirs.craftRoot() + "/lib"
        self.subinfo.options.configure.args = "--enable-shared --disable-static --with-opensp-includes=" + openSPIncludeDir + " --with-opensp-libs=" + openSPLibDir

if CraftCore.compiler.isGCCLike():
    class Package(PackageAutotools):
        def __init__(self):
            PackageAutotools.__init__(self)
else:
    class Package(CMakePackageBase):
        def __init__(self):
            # we use subinfo for now too
            CMakePackageBase.__init__(self)
