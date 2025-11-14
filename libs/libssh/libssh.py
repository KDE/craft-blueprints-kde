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
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "git://git.libssh.org/projects/libssh.git"

        for ver in ["0.9.5", "0.11.3"]:
            major, minor, patch = ver.split(".")
            self.targets[ver] = f"https://www.libssh.org/files/{major}.{minor}/libssh-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libssh-{ver}"
        self.targetDigests["0.9.5"] = (["acffef2da98e761fc1fd9c4fddde0f3af60ab44c4f5af05cd1b2d60a3fa08718"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.11.3"] = (["7d8a1361bb094ec3f511964e78a5a4dba689b5986e112afabe4f4d0d6c6125c3"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["0.9.5"] = [("fix-clang15.patch", 1)]
        self.defaultTarget = "0.11.3"

        self.releaseManagerId = 1729
        self.description = "a working SSH implementation by the mean of a library"
        self.webpage = "https://www.libssh.org/"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/openssl"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DWITH_EXAMPLES:BOOL=OFF"]
