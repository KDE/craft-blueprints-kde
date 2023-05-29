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

import shutil

import info


class subinfo(info.infoclass):
    def setTargets(self):
        # not used  yet only for reference
        self.targets["master"] = ""
        self.description = "The d3dcompiler*.dll for qml"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/mingw-w64"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def fetch(self):
        return True

    def unpack(self):
        return True

    def install(self):
        destdir = os.path.join(self.installDir(), "bin")
        utils.createDir(destdir)

        with utils.ScopedEnv({"PATHEXT": ";".join(f"_{ver}.dll" for ver in range(60, 30, -1))}):
            d3dcompiler = shutil.which("d3dcompiler")
            return utils.copyFile(d3dcompiler, os.path.join(destdir, os.path.basename(d3dcompiler)), linkOnly=False)
