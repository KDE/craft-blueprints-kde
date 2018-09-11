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

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/libjpeg-turbo/libjpeg-turbo.git"

        for ver in ["1.5.1", "1.5.3"]:
            self.targets[ver] = "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/%s.tar.gz" % ver
            self.archiveNames[ver] = "libjpeg-turbo-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'libjpeg-turbo-%s' % ver

        self.targetDigests['1.5.1'] = (
            ['c15a9607892113946379ccea3ca8b85018301b200754f209453ab21674268e77'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.5.3'] = (
            ['1a17020f859cb12711175a67eab5c71fc1904e04b587046218e36106e07eabde'], CraftHash.HashAlgorithm.SHA256)
        self.description = "libjpeg-turbo is a JPEG image codec that uses SIMD instructions (MMX, SSE2, NEON, AltiVec) to accelerate baseline JPEG compression and decompression on x86, x86-64, ARM, and PowerPC systems"
        self.webpage = "http://libjpeg-turbo.virtualgl.org/"
        self.defaultTarget = '1.5.3'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-utils/nasm"] = "default"


from Package.CMakePackageBase import *


from Package.AutoToolsPackageBase import *
from Package.CMakePackageBase import *

class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        # Version 2 uses cmake
        self.subinfo.options.configure.bootstrap = True
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args = "--disable-shared --enable-static "
        else:
            self.subinfo.options.configure.args = "--enable-shared --disable-static "
        self.subinfo.options.configure.args += f"--disable-doc-build NASM={CraftCore.cache.findApplication('nasm')}"

if CraftCore.compiler.isUnix:
    class Package(PackageAutotools):
        def __init__(self):
            PackageAutotools.__init__(self)
else:
    class Package(CMakePackageBase):
        def __init__(self):
            CMakePackageBase.__init__(self)
