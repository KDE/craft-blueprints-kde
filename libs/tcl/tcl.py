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
from Package.AutoToolsPackageBase import *
from Package.MSBuildPackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['8-6-8']:
            self.targets[ver] = 'https://github.com/tcltk/tcl/archive/core-%s.zip' % ver
            self.archiveNames[ver] = "core-%s.zip" % ver
            self.targetInstSrc[ver] = 'tcl-core-%s' % ver

        self.targetDigests['8-6-8'] = (['7d4b0aea18142dce44a34f366ed251e50d4edba8918894adf0fab7a932a1f80d'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '8-6-8'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = "default"

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

    def install(self):
        if CraftCore.compiler.isMinGW():
            shutil.copy(os.path.join(self.buildDir(), "tclsh86.exe"), os.path.join(CraftCore.standardDirs.craftBin(), "tclsh.exe")) # otherwise super().install() fails
            shutil.copy(os.path.join(self.buildDir(), "tclsh86.exe"), os.path.join(CraftCore.standardDirs.craftBin(), "tclsh8.6.exe"))
        isInstalled = super().install()
        if isInstalled and not CraftCore.compiler.isMinGW():
            shutil.copy(os.path.join(self.installDir(), "bin", "tclsh8.6"), os.path.join(self.installDir(), "bin", "tclsh"))
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
