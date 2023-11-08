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
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.110.0"] = [("KDEInstallDirs6 fix BUNDLE destination.patch", 1)]
        self.patchLevel["5.110.0"] = 1

        # Fix Windows target version, see https://invent.kde.org/frameworks/extra-cmake-modules/-/merge_requests/399
        self.patchToApply["5.245.0"] = [("399.diff", 1)]
        self.patchToApply["master"] = [("399.diff", 1)]
        self.patchLevel["master"] = 1

        self.tags = "ECM"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if CraftCore.compiler.isWindows:
            self.buildDependencies["dev-utils/icoutils"] = None
        # needed for many kf5's
        self.buildDependencies["dev-utils/flexbison"] = None

        if CraftCore.settings.getboolean("CMake", "KDE_L10N_AUTO_TRANSLATIONS", False):
            self.buildDependencies["dev-utils/ruby"] = None

        if CraftCore.compiler.isAndroid:
            self.buildDependencies["python-modules/requests"] = None
            self.buildDependencies["python-modules/pyxdg"] = None
            self.buildDependencies["python-modules/pyyaml"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
