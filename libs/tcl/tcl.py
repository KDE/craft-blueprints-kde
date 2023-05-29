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

import shutil
import stat

import info
from Package.AutoToolsPackageBase import *
from Package.MSBuildPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["8-6-8", "8-6-11"]:
            self.targets[ver] = f"https://github.com/tcltk/tcl/archive/core-{ver}.tar.gz"
            self.archiveNames[ver] = f"core-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"tcl-core-{ver}"

        self.targetDigests['8-6-8'] = (['5e9da63f535cee07bfbc6d9f12a657b1065911e473550dc74968025bc5a0e447'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['8-6-11'] = (['3b49ef3316bda17c1e004f0ea1aa5ba8fb3292329e923e7043147f99739b3241'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "8-6-11"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None

class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.noDataRootDir = True
        self.subinfo.options.configure.args += " --disable-static --enable-shared --enable-threads --enable-64bit "

        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.projectFile = "win/configure"
        else:
            self.subinfo.options.configure.projectFile = "unix/configure"

        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += " --enable-framework --disable-corefoundation "

    def configure(self):
        isConfigured = super().configure()
        if isConfigured and CraftCore.compiler.isMinGW():
            Makefile = os.path.join(self.buildDir(), "Makefile")

            with open(Makefile, "rt") as f:
                content = f.read()

            content = content.replace(r"INSTALL_ROOT	=", r"INSTALL_ROOT	= %s" % OsUtils.toMSysPath(self.installDir()))
            content = content.replace(r"$(INSTALL_ROOT)$(bindir)", r"$(INSTALL_ROOT)/bin")
            content = content.replace(r"$(INSTALL_ROOT)$(libdir)", r"$(INSTALL_ROOT)/lib")
            content = content.replace(r"$(INSTALL_ROOT)$(includedir)", r"$(INSTALL_ROOT)/include")
            content = content.replace(r"$(INSTALL_ROOT)$(mandir)", r"$(INSTALL_ROOT)/share/man")
            content = content.replace(r"$(INSTALL_ROOT)$(TCL_LIBRARY)", r"$(INSTALL_ROOT)/lib/tcl$(VERSION)")

            with open(Makefile, "wt") as f:
                f.write(content)

        return isConfigured

    def install(self):
        if CraftCore.compiler.isMinGW():
            shutil.copy(os.path.join(self.buildDir(), "tclsh86.exe"), os.path.join(CraftCore.standardDirs.craftRoot(), "bin", "tclsh.exe")) # otherwise super().install() fails
            shutil.copy(os.path.join(self.buildDir(), "tclsh86.exe"), os.path.join(CraftCore.standardDirs.craftRoot(), "bin", "tclsh8.6.exe"))

        isInstalled = super().install()

        if isInstalled:
            if CraftCore.compiler.isMinGW():
                shutil.copy(os.path.join(self.installDir(), "bin", "tclsh8.6"), os.path.join(self.installDir(), "bin", "tclsh"))

            if CraftCore.compiler.isLinux:
                os.chmod(os.path.join(self.installDir(), "lib", "libtcl8.6.so"), stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            elif CraftCore.compiler.isMacOS:
                os.chmod(os.path.join(self.installDir(), "lib", "libtcl8.6.dylib"), stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

        return isInstalled

class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)

    def make(self):
        os.chdir(os.path.join(self.sourceDir(), "win"))
        return utils.system(f"nmake -f makefile.vc release INSTALLDIR={self.installDir()}")

    def install(self):
        os.chdir(os.path.join(self.sourceDir(), "win"))
        isInstalled = utils.system(f"nmake -f makefile.vc install INSTALLDIR={self.installDir()}")
        if isInstalled:
            utils.copyFile(os.path.join(self.installDir(), "bin", "tclsh86t.exe"),
                           os.path.join(self.installDir(), "bin", "tclsh.exe"))
            utils.copyFile(os.path.join(self.installDir(), "bin", "tcl86t.dll"),
                           os.path.join(self.installDir(), "bin", "tcl86.dll"))
            utils.copyFile(os.path.join(self.installDir(), "lib", "tcl86t.lib"),
                           os.path.join(self.installDir(), "lib", "tcl86.lib"))


        return isInstalled

if CraftCore.compiler.isGCCLike():
    class Package(PackageAutotools):
        def __init__(self):
            PackageAutotools.__init__(self)
else:
    class Package(PackageMSVC):
        def __init__(self):
            PackageMSVC.__init__(self)
