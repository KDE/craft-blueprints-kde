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
        self.targets['0.9.13'] = "http://downloads.sourceforge.net/project/libofx/libofx/libofx-0.9.13.tar.gz"
        self.targetDigests['0.9.13'] = (['57eaf97cddbaf82c24f26b8f5cf8b2fbfd4969c74500a2c9acc9082b83bcc0e4'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc['0.9.13'] = "libofx-0.9.13"
        self.patchToApply['0.9.13'] = [("libofx-0.9.13-20180505-1.diff", 1)]
        self.patchToApply['0.9.13'] += [("libofx-0.9.12-20180412.diff", 1)]
        if CraftCore.compiler.isMSVC():
            self.patchToApply['0.9.13'] += [("libofx-0.9.13-20180505-2.diff", 1)]
            self.patchToApply['0.9.13'] += [("libofx-0.9.13-20180505-3.diff", 1)]
            self.patchToApply['0.9.13'] += [("libofx-0.9.13-20180505-5.diff", 1)]

        if CraftCore.compiler.isMSVC() or CraftCore.compiler.isMinGW():
            self.patchToApply['0.9.13'] += [("libofx-0.9.13-20180505-4.diff", 1)]

        self.description = "a parser and an API for the OFX (Open Financial eXchange) specification"
        self.defaultTarget = '0.9.13'

    def setDependencies(self):
        self.runtimeDependencies["libs/libopensp"] = None
        self.runtimeDependencies["libs/iconv"] = None


from Package.AutoToolsPackageBase import *
from Package.CMakePackageBase import *

class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        openSPIncludeDir = CraftStandardDirs.craftRoot() + "/include/OpenSP"
        openSPLibDir = CraftStandardDirs.craftRoot() + "/lib"
        self.subinfo.options.configure.args = "--enable-shared --disable-static --with-opensp-includes=" + openSPIncludeDir + " --with-opensp-libs=" + openSPLibDir

if CraftCore.compiler.isMacOS:
    class Package(PackageAutotools):
        def __init__(self):
            PackageAutotools.__init__(self)
else:
    class Package(CMakePackageBase):
        def __init__(self):
            # we use subinfo for now too
            CMakePackageBase.__init__(self)
