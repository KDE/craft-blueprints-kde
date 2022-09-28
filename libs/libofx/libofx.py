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
        self.targets['0.10.8'] = "https://github.com/libofx/libofx/releases/download/0.10.8/libofx-0.10.8.tar.gz"
        self.targetDigests['0.10.8'] = (['d7133fb939ac0e46507cf7a5de7678b52bf6bcc7be87adc94b761c2cd12ce320'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc['0.10.8'] = "libofx-0.10.8"

        self.description = "a parser and an API for the OFX (Open Financial eXchange) specification"
        self.defaultTarget = '0.10.8'
        self.patchToApply['0.10.8'] = ('0001-Fix-library-name-on-Windows.patch', 1)
        self.patchLevel['0.10.8'] = 1

    def setDependencies(self):
        self.runtimeDependencies["libs/libopensp"] = None
        self.runtimeDependencies["libs/iconv"] = None


from Package.AutoToolsPackageBase import *
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        # we use subinfo for now too
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DENABLE_OFXCONNECT=off -DENABLE_OFX2QIF=off"
