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
from Package.AutoToolsPackageBase import *
from Utils.PostInstallRoutines import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.9"]:
            self.targets[ver] = f"http://freedesktop.org/~hadess/shared-mime-info-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"shared-mime-info-{ver}"
        self.patchLevel["1.9"] = 3
        self.targetDigests["1.9"] = (['5c0133ec4e228e41bdf52f726d271a2d821499c2ab97afd3aa3d6cf43efcdc83'], CraftHash.HashAlgorithm.SHA256)

        self.description = "The shared-mime-info package contains the core database of common types and the update-mime-database command used to extend it"
        self.webpage = "https://www.freedesktop.org/wiki/Software/shared-mime-info/"
        self.defaultTarget = "1.9"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = "default"
        self.buildDependencies["dev-utils/intltool"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/gettext"] = "default"
        self.runtimeDependencies["libs/libxml2"] = "default"
        self.runtimeDependencies["libs/glib"] = "default"
        self.runtimeDependencies["libs/zlib"] = "default"
        if CraftCore.compiler.isMSVC():
            self.runtimeDependencies["kdesupport/kdewin"] = "default"


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        root = self.shell.toNativePath(CraftCore.standardDirs.craftRoot())
        self.subinfo.options.configure.args += f" --disable-default-make-check --disable-update-mimedb"
        self.subinfo.options.configure.cflags = f"-I{root}/include/glib-2.0 -I{root}/include/libxml2"
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.cflags += f" -I{root}/include/msvc"
            self.shell.useMSVCCompatEnv = True
            self.platform = ""
            self.subinfo.options.configure.args += f" PKG_CONFIG=':' "
            self.subinfo.options.configure.ldflags ="-lglib-2.0 -lgobject-2.0 -lgio-2.0 -lgthread-2.0 -llibxml2 -lintl -lzlib"
            if self.buildType() == "Debug":
                self.subinfo.options.configure.ldflags += " -lkdewind"
            else:
                self.subinfo.options.configure.ldflags += " -lkdewin"

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMSVC() and self.buildType() == "Debug":
            return utils.copyFile(os.path.join(self.buildDir(), "update-mime-database.pdb"), os.path.join(self.installDir(), "bin", "update-mime-database.pdb"))
        if OsDetection.isWin():
            manifest = os.path.join(self.packageDir(), "update-mime-database.exe.manifest")
            executable = os.path.join(self.installDir(), "bin", "update-mime-database.exe")
            utils.embedManifest(executable, manifest)
        return True

    def postQmerge(self):
        return PostInstallRoutines.updateSharedMimeInfo(self)
