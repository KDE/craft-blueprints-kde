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
from Package.MesonPackageBase import *
from Utils.PostInstallRoutines import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ["2.2"]:
            self.targets[ver] = f"https://gitlab.freedesktop.org/xdg/shared-mime-info/-/archive/{ver}/shared-mime-info-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"shared-mime-info-{ver}"
        self.targetDigests["2.2"] = (["418c480019d9865f67f922dfb88de00e9f38bf971205d55cdffab50432919e61"], CraftHash.HashAlgorithm.SHA256)

        self.description = "The shared-mime-info package contains the core database of common types and the update-mime-database command used to extend it"
        self.webpage = "https://www.freedesktop.org/wiki/Software/shared-mime-info/"
        self.defaultTarget = "2.2"

        if CraftCore.compiler.isMSVC():
            self.patchToApply["2.2"] = [("disable-translation.patch", 1), ("cpp.patch", 1)]

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/intltool"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        if CraftCore.compiler.isMSVC():
            self.runtimeDependencies["kdesupport/kdewin"] = None

class Package(MesonPackageBase):
    def __init__(self):
        MesonPackageBase.__init__(self)

    def install(self):
        if not super().install():
            return False
        # must be called before we sign
        if CraftCore.compiler.isWindows:
            manifest = os.path.join(self.packageDir(), "update-mime-database.exe.manifest")
            executable = os.path.join(self.installDir(), "bin", "update-mime-database.exe")
            utils.embedManifest(executable, manifest)
        return True

    def postQmerge(self):
        return PostInstallRoutines.updateSharedMimeInfo(self)
