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
import glob

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["5.2.3"]:
            self.targets[ver] = f"http://tukaani.org/xz/xz-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"xz-{ver}"

        self.targetDigests["5.2.3"] = (['7876096b053ad598c31f6df35f7de5cd9ff2ba3162e5a5554e4fc198447e0347'], CraftHash.HashAlgorithm.SHA256)

        self.description = "free general-purpose data compression software with high compression ratio"
        self.webpage = "https://tukaani.org/xz"
        self.defaultTarget = ver

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.MSBuildPackageBase import *


class PackageMSBuild(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)
        self.subinfo.options.configure.projectFile = os.path.join(self.sourceDir(), "windows", "xz_win.sln")
        self.msbuildTargets = ["liblzma_dll"]


    def install(self):
        if not MSBuildPackageBase.install(self, installHeaders=False):
            return False

        headerDir = os.path.join(self.sourceDir(), "src", "liblzma", "api")
        includeDir = os.path.join(self.installDir(), "include")
        header = glob.glob(os.path.join(headerDir, f"**/*.h"), recursive=True)
        for h in header:
            utils.copyFile(h, h.replace(headerDir, includeDir), linkOnly=False)
        return True

from Package.AutoToolsPackageBase import *

class PackageAutotools(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --disable-static --enable-shared "


if CraftCore.compiler.isMSVC():
    class Package(PackageMSBuild):
        pass
else:
    class Package(PackageAutotools):
        pass
