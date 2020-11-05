# -*- coding: utf-8 -*-
# Copyright 2018 Hannah von Reth <vonreth@kde.org>
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
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "3.30.1"
        sqlVer = "3300100"
        self.patchToApply[ver] = [ ("sqlite-3.26.0-20181216.diff", 1)]
        self.targets[ver] = f"https://sqlite.org/2019/sqlite-amalgamation-{sqlVer}.zip"
        self.targetInstSrc[ver] = f"sqlite-amalgamation-{sqlVer}"
        self.targetDigests["3.30.1"] = (['adf051d4c10781ea5cfabbbc4a2577b6ceca68590d23b58b8260a8e24cc5f081'], CraftHash.HashAlgorithm.SHA256)

        self.targets["3.31.1"] = "https://sqlite.org/2020/sqlite-amalgamation-3310100.zip"
        self.targetInstSrc["3.31.1"] = "sqlite-amalgamation-3310100"
        self.patchToApply["3.31.1"] = [ ("sqlite-3.26.0-20181216.diff", 1), ("sqlite-3.31.1-20201026.diff", 1)]
        self.targetDigests["3.31.1"] = (['f3c79bc9f4162d0b06fa9fe09ee6ccd23bb99ce310b792c5145f87fbcc30efca'], CraftHash.HashAlgorithm.SHA256)

        self.description = "a library providing a self-contained, serverless, zero-configuration, transactional SQL database engine"
        self.patchLevel["3.30.1"] = 2
        self.patchLevel["3.31.1"] = 1
        self.defaultTarget = "3.31.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
