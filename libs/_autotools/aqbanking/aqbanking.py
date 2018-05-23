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
from Package.AutoToolsPackageBase import *
from CraftOS.osutils import OsUtils

class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["5.7.8"] = "https://www.aquamaniac.de/sites/download/download.php?package=03&release=217&file=02&dummy=aqbanking-5.7.8.tar.gz"
        self.targetDigests["5.7.8"] = (['16f86e4cc49a9eaaa8dfe3206607e627873208bce45a70030c3caea9b5afc768'], CraftHash.HashAlgorithm.SHA256)
        self.archiveNames["5.7.8"] = "aqbanking-5.7.8.tar.gz"
        self.targetInstSrc["5.7.8"] = "aqbanking-5.7.8"
        self.defaultTarget = "5.7.8"
        self.patchLevel["5.7.8"] = 1

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/ktoblzcheck"] = "default"
        self.runtimeDependencies["libs/gwenhywfar"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = "default"

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
        # this prevents "cannot find the library libaqhbci.la or unhandled argument libaqhbci.la"
        self.subinfo.options.make.supportsMultijob = False

    def postInstall(self):

        cmakes = [ os.path.join(self.installDir(), "lib", "cmake", f"aqbanking-{self.subinfo.defaultTarget[:-2]}", "aqbanking-config.cmake") ]
        for cmake in cmakes:
            f = open(cmake, "r+")
            cmakeFileContents = f.readlines()
            for i in range(len(cmakeFileContents)):
                if CraftCore.compiler.isMinGW():
                    m = re.search('set_and_check\(prefix "(?P<root>[^"]*)"\)', cmakeFileContents[i])
                    if m is not None:
                        craftRoot = OsUtils.toUnixPath(CraftStandardDirs.craftRoot())
                        if craftRoot.endswith("/"):
                            craftRoot = craftRoot[:-1]
                        cmakeFileContents[i] = cmakeFileContents[i].replace(m.group('root'), craftRoot)

                    m2 = re.search("libaqbanking.so", cmakeFileContents[i])
                    if m2 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace("lib/libaqbanking.so", "bin/libaqbanking-35.dll")
                elif CraftCore.compiler.isMacOS:
                    m2 = re.search("libaqbanking.so", cmakeFileContents[i])
                    if m2 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace("libaqbanking.so", "libaqbanking.35.dylib")
            f.seek(0)
            f.write(''.join(cmakeFileContents))
            f.close()
        return AutoToolsPackageBase.postInstall(self)
