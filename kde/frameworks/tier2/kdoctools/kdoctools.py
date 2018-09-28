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
        self.versionInfo.setDefaultValues()
        self.description = "Documentation generation from docbook "

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-utils/perl"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["libs/libxslt"] = "default"
        self.runtimeDependencies["data/docbook-dtd"] = "default"
        self.runtimeDependencies["data/docbook-xsl"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def postInstall(self):
        if not CraftCore.compiler.isWindows:
            return True
        return self.patchInstallPrefix([os.path.join(self.installDir(), CraftCore.standardDirs.locations.data, "kf5/kdoctools/customization/xsl/all-l10n.xml")],
                                       OsUtils.toUnixPath(self.subinfo.buildPrefix), OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()))

