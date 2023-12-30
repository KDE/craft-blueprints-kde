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
import utils
from CraftCore import CraftCore
from Utils.PostInstallRoutines import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ["2.3"]:
            self.targets[ver] = f"https://gitlab.freedesktop.org/xdg/shared-mime-info/-/archive/{ver}/shared-mime-info-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"shared-mime-info-{ver}"
        self.targetDigests["2.3"] = (["96ac085d82e2e654e40e34c13d97b74f6657357ee6b443d922695adcf548961c"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["2.3"] = [("12a3a6b1141c704fc594379af1808bb9008d588c.patch", 1), ("7499ac1a85b2487b94e315e6b55c34bcf220295f.patch", 1)]
        if CraftCore.compiler.isMSVC():
            self.patchToApply["2.3"] += [("disable-translation.patch", 1)]

        self.patchLevel["2.3"] = 1

        self.description = "The shared-mime-info package contains the core database of common types and the update-mime-database command used to extend it"
        self.webpage = "https://www.freedesktop.org/wiki/Software/shared-mime-info/"
        self.defaultTarget = "2.3"

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


from Package.MesonPackageBase import *


class Package(MesonPackageBase):
    def __init__(self):
        MesonPackageBase.__init__(self)
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.dynamic.buildTests = False

        if CraftCore.compiler.isWindows:
            # stripping a embedManifest patched binary fails
            self.subinfo.options.package.disableStriping = True

        if not self.subinfo.options.dynamic.buildTests:
            self.subinfo.options.configure.args += ["-Dbuild-tests=false"]

    def install(self):
        if not super().install():
            return False
        # must be called before we sign
        if CraftCore.compiler.isWindows:
            manifest = os.path.join(self.blueprintDir(), "update-mime-database.exe.manifest")
            executable = os.path.join(self.installDir(), "bin", "update-mime-database.exe")
            utils.embedManifest(executable, manifest)
        return True

    def postQmerge(self):
        return PostInstallRoutines.updateSharedMimeInfo(self)
