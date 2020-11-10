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
import re
import CraftCore

from Package.AutoToolsPackageBase import *
from Package.BinaryPackageBase import *

if not CraftCore.compiler.isMSVC():
    class subinfo(info.infoclass):
        def setTargets( self ):
            self.versionInfo.setDefaultValues()
            
            self.targetDigests["1.9.0"] = (["1b29fedb8bfad775e70eafac5b0590621683b2d9869db994568e6401f4034ceb"], CraftHash.HashAlgorithm.SHA256)
            self.targetDigests["1.11.1"] = (["2d1b111774d2e3dd26dcd7c251819ce4ef774ec5e566251eb9308fa7542fbd6f"], CraftHash.HashAlgorithm.SHA256)
            self.targetDigests["1.14.0"] = (['cef1f710a6b0d28f5b44242713ad373702d1466dcbe512eb4e754d7f35cd4307'], CraftHash.HashAlgorithm.SHA256)
            self.patchToApply["1.9.0"] = [("gpgme-1.9.0-20170801.diff", 1)]
            self.patchToApply["1.11.1"] = [("gpgme-1.1.11-20170801.diff", 1),
                                        ("qt Respect --disable-gpg-test for tests.patch", 1),
                                        ("gpgme-1.11.1-20180820.diff", 1),# disable the documentation (crashes on x86)
                                        ("gpgme-1.11.1-20180920.diff", 1),# fix qgpgme config
                                        ]
            if CraftCore.compiler.isWindows:
                self.patchToApply["1.11.1"] += [("gpgme-1.1.11-20180620.diff", 1)]

            self.patchLevel["1.11.1"] = 5
            
        def setDependencies( self ):
            self.buildDependencies["dev-utils/msys"] = None
            self.runtimeDependencies["virtual/base"] = None
            self.runtimeDependencies["libs/gpg-error"] = None
            self.runtimeDependencies["libs/assuan2"] = None


    class Package(AutoToolsPackageBase):
        def __init__( self, **args ):
            AutoToolsPackageBase.__init__( self )
            self.subinfo.options.configure.args += ["--enable-languages=no", "--disable-gpg-test"]

        def install(self):
            if not super().install():
                return False
            if CraftCore.compiler.isWindows:
                return utils.mergeTree(self.installDir() / "libexec", self.installDir() / "bin")
            return True

        def postInstall(self):
            badFiles = [os.path.join(self.installDir(), "bin", "gpgme-config")]
            return self.patchInstallPrefix(badFiles,
                                            [OsUtils.toMSysPath(self.subinfo.buildPrefix), OsUtils.toUnixPath(self.subinfo.buildPrefix)],
                                            CraftCore.standardDirs.craftRoot())

else:
    class subinfo(info.infoclass):
        def setTargets(self):
            self.addCachedAutotoolsBuild(versionInfo="../../_msvc/version.ini")

        def setDependencies(self):
            self.runtimeDependencies['virtual/base'] = None
            self.runtimeDependencies["libs/mingw-crt4msvc"] = None
            self.runtimeDependencies['libs/assuan2'] = None
            self.runtimeDependencies["libs/gpg-error"] = None



    class Package(BinaryPackageBase):
        def __init__(self, **args):
            BinaryPackageBase.__init__(self)
