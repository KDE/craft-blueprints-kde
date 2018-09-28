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
        if CraftCore.compiler.isMacOS:
            self.targets['1.3.0'] = "http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz"
            self.targetDigests['1.3.0'] = (['3dce6601b495f5b3d45b59f7d2492a340ee7e84b5beca17e48f862502bd5603f'], CraftHash.HashAlgorithm.SHA256)
            self.targetInstSrc['1.3.0'] = "yasm-1.3.0"
        elif CraftCore.compiler.isX64():
            if CraftCore.compiler.isMinGW():
                self.targets['1.3.0'] = "http://www.tortall.net/projects/yasm/releases/yasm-1.3.0-win64.exe"
            if CraftCore.compiler.isMSVC():
                self.targets['1.3.0'] = "http://www.tortall.net/projects/yasm/releases/vsyasm-1.3.0-win64.zip"
        else:
            if CraftCore.compiler.isMinGW():
                self.targets['1.3.0'] = "http://www.tortall.net/projects/yasm/releases/yasm-1.3.0-win32.exe"
            if CraftCore.compiler.isMSVC():
                self.targets['1.3.0'] = "http://www.tortall.net/projects/yasm/releases/vsyasm-1.3.0-win32.zip"

        if CraftCore.compiler.isMacOS:
            self.targetInstallPath["1.3.0"] = "dev-utils"
        else:
            self.targetInstallPath["1.3.0"] = os.path.join("dev-utils", "bin")

        self.description = "The Yasm Modular Assembler Project"
        self.defaultTarget = '1.3.0'

    def setDependencies(self):
        if CraftCore.compiler.isMacOS:
            self.buildDependencies["libs/gettext"] = None
            self.buildDependencies["libs/iconv"] = None
            self.buildDependencies["dev-utils/intltool"] = None

        self.runtimeDependencies["virtual/bin-base"] = None


from Package.AutoToolsPackageBase import *
from Package.BinaryPackageBase import *

class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)

class BinaryPackage(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)
        
    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        if CraftCore.compiler.isMinGW_W32():
            shutil.move(os.path.join(self.installDir(), "yasm-1.3.0-win32.exe"),
                        os.path.join(self.installDir(), "yasm.exe"))
        if CraftCore.compiler.isMinGW_W64():
            shutil.move(os.path.join(self.installDir(), "yasm-1.3.0-win64.exe"),
                        os.path.join(self.installDir(), "yasm.exe"))
        
        return True


if CraftCore.compiler.isMacOS:
    class Package(PackageAutotools):
        def __init__(self):
            PackageAutotools.__init__(self)
else:
    class Package(BinaryPackage):
        def __init__(self):
            BinaryPackage.__init__(self)
            ## @todo remove the readme.txt file
