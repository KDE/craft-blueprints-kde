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
        self.targets["6.1.2"] = "https://www.aquamaniac.de/rdm/attachments/download/269/aqbanking-6.1.2.tar.gz"
        self.targetDigests["6.1.2"] = (['0b54c70a8ab1bd5537d8b26d05a9e44db0600b64d8cbb63c34018dee11f67190'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["6.1.2"] = "aqbanking-6.1.2"
        self.defaultTarget = "6.1.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gwenhywfar"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
        # this prevents "cannot find the library libaqhbci.la or unhandled argument libaqhbci.la"
        self.subinfo.options.make.supportsMultijob = False

        # Including libtool from the newer autotools in craftroot breaks the build (at least on macOS)
        self.subinfo.options.configure.autoreconf = False

    def postInstall(self):
        cmakes = [ os.path.join(self.installDir(), "lib", "cmake", f"aqbanking-{self.subinfo.buildTarget[:-2]}", "aqbanking-config.cmake") ]
        for cmake in cmakes:
            with open(cmake, "rt") as f:
                cmakeFileContents = f.readlines()
            for i in range(len(cmakeFileContents)):
                if CraftCore.compiler.isMinGW():
                    m = re.search('set_and_check\(prefix "(?P<root>[^"]*)"\)', cmakeFileContents[i])
                    if m is not None:
                        craftRoot = OsUtils.toUnixPath(CraftStandardDirs.craftRoot())
                        if craftRoot.endswith("/"):
                            craftRoot = craftRoot[:-1]
                        cmakeFileContents[i] = cmakeFileContents[i].replace(m.group('root'), craftRoot)
                elif CraftCore.compiler.isMacOS:
                    m2 = re.search("(libaqbanking.so.(\d*))", cmakeFileContents[i])
                    if m2 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace(m2.group(1), "libaqbanking.%s.dylib" % m2.group(2))
            with open(cmake, "wt") as f:
                f.write(''.join(cmakeFileContents))
        return AutoToolsPackageBase.postInstall(self)
