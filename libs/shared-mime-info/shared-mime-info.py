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
        for ver in ["1.9", "1.15", "2.1"]:
            self.targets[ver] = f"https://gitlab.freedesktop.org/xdg/shared-mime-info/-/archive/2.1/shared-mime-info-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"shared-mime-info-{ver}"
        self.patchLevel["1.9"] = 3
        self.targetDigests["1.9"] = (['5c0133ec4e228e41bdf52f726d271a2d821499c2ab97afd3aa3d6cf43efcdc83'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.15"] = (['f482b027437c99e53b81037a9843fccd549243fd52145d016e9c7174a4f5db90'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.1"] = (['37df6475da31a8b5fc63a54ba0770a3eefa0a708b778cb6366dccee96393cb60'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.1"] = [("shared-mime-info-2.1-20210421.diff", 1)]

        self.description = "The shared-mime-info package contains the core database of common types and the update-mime-database command used to extend it"
        self.webpage = "https://www.freedesktop.org/wiki/Software/shared-mime-info/"
        self.defaultTarget = "2.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        

from Package.MesonPackageBase import *

class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)