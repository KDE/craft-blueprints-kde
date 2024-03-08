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

import os
import re

import info
import utils
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.MSBuildPackageBase import MSBuildPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.4.2"]:
            self.targets[ver] = f"https://github.com/sqlcipher/sqlcipher/archive/v{ver}.zip"
            self.archiveNames[ver] = f"sqlcipher-{ver}.zip"
            self.targetInstSrc[ver] = f"sqlcipher-{ver}"
            self.patchLevel[ver] = 6

        self.targetDigests["3.4.2"] = (["f2afbde554423fd3f8e234d21e91a51b6f6ba7fc4971e73fdf5d388a002f79f1"], CraftHash.HashAlgorithm.SHA256)

        if CraftCore.compiler.isWindows:
            self.patchToApply["3.4.2"] = [("sqlcipher-3.4.2-20180727.diff", 1)]

        self.defaultTarget = "3.4.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/tcl"] = None
        self.runtimeDependencies["libs/icu"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


# warning: empty sqlite3.h can prevent successfull build
class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--enable-tempstore=yes"]
        if CraftCore.compiler.isMinGW():
            self.subinfo.options.make.supportsMultijob = False
            self.subinfo.options.configure.args += ["CFLAGS='-DSQLITE_HAS_CODEC'"]
        else:
            self.subinfo.options.configure.args += ["CFLAGS=-DSQLITE_HAS_CODEC"]

    def configure(self):
        isConfigured = super().configure()
        if isConfigured and CraftCore.compiler.isMinGW():
            Makefile = self.buildDir() / "Makefile"

            with open(Makefile, "rt") as f:
                content = f.read()

            m = re.search("TCLLIBDIR = (?P<absolutePath>.*)", content)
            if not m:
                return False

            relativePath = os.path.relpath(m.group("absolutePath"), CraftCore.standardDirs.craftRoot())
            relativePath = relativePath.replace("\\", "/")

            content = content.replace(r"$(DESTDIR)$(bindir)", r"$(DESTDIR)/bin")
            content = content.replace(r"$(DESTDIR)$(libdir)", r"$(DESTDIR)/lib")
            content = content.replace(r"$(DESTDIR)$(includedir)", r"$(DESTDIR)/include/sqlcipher")
            content = content.replace(r"$(DESTDIR)$(mandir)", r"$(DESTDIR)/share/man")
            content = content.replace(r"$(DESTDIR)$(TCLLIBDIR)", r"$(DESTDIR)/" + relativePath)
            content = content.replace(r"$(DESTDIR)$(pkgconfigdir)", r"$(DESTDIR)/lib/pkgconfig")

            with open(Makefile, "wt") as f:
                f.write(content)

        return isConfigured

    def postInstall(self):
        if CraftCore.compiler.isMinGW():
            cmakes = [self.installDir() / "lib/pkgconfig/sqlcipher.pc"]
        else:
            cmakes = []
        return self.patchInstallPrefix(cmakes, OsUtils.toMSysPath(self.subinfo.buildPrefix)[:-1], OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())[:-1])


class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **args):
        super().__init__()

    def configure(self):
        self.enterSourceDir()
        fileName = "Makefile.msc"
        with open(fileName, "rt") as f:
            content = f.read()

        # recipe taken from https://github.com/sqlitebrowser/sqlitebrowser/wiki/Win64-setup-%E2%80%94-Compiling-SQLCipher

        # libname_EXPORTS is cmake variable. It allows to use __declspec(dllexport) while building this library
        # and __declspec(dllimport) while linking to this library
        defines = "TCC = $(TCC) -DSQLITE_HAS_CODEC -Dlibsqlcipher_EXPORTS\n" "RCC = $(RCC) -DSQLITE_HAS_CODEC -Dlibsqlcipher_EXPORTS\n"

        includeDir = CraftCore.standardDirs.craftRoot() / "include"
        libDir = CraftCore.standardDirs.craftRoot() / "lib"
        binDir = CraftCore.standardDirs.craftRoot() / "bin"
        includeDirs = f"TCC = $(TCC) -I{includeDir}\n" f"RCC = $(RCC) -I{includeDir}\n"

        index = content.find("TCC = $(TCC) -DSQLITE_TEMP_STORE=1")
        content = content[:index] + defines + includeDirs + content[index:]

        includeLibs = f"LTLIBPATHS = $(LTLIBPATHS) /LIBPATH:{libDir}\n" "LTLIBS = $(LTLIBS) libssl.lib libcrypto.lib tcl86.lib\n"

        index = content.find("# If ICU support is enabled, add the linker options for it.")
        content = content[:index] + includeLibs + content[index:]

        content = content.replace(r"-DSQLITE_TEMP_STORE=1", r"-DSQLITE_TEMP_STORE=2")

        # stops segfaulting each time in qsqlcipher-test in KMyMoney with this, but is still unstable with core application
        content = content.replace(r"USE_CRT_DLL = 0", r"USE_CRT_DLL = 1")

        content = content.replace(r"DYNAMIC_SHELL = 0", r"DYNAMIC_SHELL = 1")

        content = content.replace(r"USE_ICU = 0", r"USE_ICU = 1")
        content = content.replace(r"c:\icu\include", includeDir)
        content = content.replace(r"c:\icu\lib", libDir)
        content = content.replace(r"c:\tcl\bin", binDir)

        content = content.replace(r"c:\tcl\include", includeDir)
        content = content.replace(r"c:\tcl\lib", libDir)

        # sqlite3.lib will be picked by next replace method
        content = content.replace(r"libsqlite3.lib", r"sqlite3.lib")

        content = content.replace(r"winsqlite3.dll", r"libsqlcipher.dll")
        content = content.replace(r"winsqlite3.lib", r"libsqlcipher.lib")
        content = content.replace(r"winsqlite3shell.exe", r"sqlcipher.exe")
        # if libraries are called "sqlcipher" then no DYNAMIC_SHELL is possible
        content = content.replace(r"sqlite3.dll", r"libsqlcipher.dll")
        content = content.replace(r"sqlite3.lib", r"libsqlcipher.lib")
        content = content.replace(r"sqlite3.exe", r"sqlcipher.exe")
        content = content.replace(r"sqlite3sh.pdb", r"sqlciphersh.pdb")
        content = content.replace(r"sqlite3.def", r"sqlcipher.def")

        with open(fileName, "wt") as f:
            f.write(content)
        return super().configure()

    def make(self):
        return utils.system(r"nmake -f Makefile.msc")

    def install(self):
        isInstalled = super().install()
        if isInstalled:
            # move sqlcipher headers to sqlcipher directory to not conflit with sqlite3
            includeDir = self.installDir() / "include"
            utils.moveFile(includeDir, self.installDir() / "sqlcipher")
            utils.createDir(includeDir)
            utils.moveFile(self.installDir() / "sqlcipher", includeDir / "sqlcipher")

            # allow finding sqlcipher library by pkgconfig module
            pkgConfigDir = self.installDir() / "lib/pkgconfig"
            pkgConfigFile = pkgConfigDir / "sqlcipher.pc"
            utils.createDir(pkgConfigDir)
            utils.copyFile(self.sourceDir() / "sqlcipher.pc.in", pkgConfigFile)
            with open(pkgConfigFile, "rt") as f:
                content = f.read()
            content = content.replace(r"@prefix@", str(CraftCore.standardDirs.craftRoot()))
            content = content.replace(r"@exec_prefix@", r"${prefix}/bin")
            content = content.replace(r"@libdir@", r"${prefix}/lib")
            content = content.replace(r"@includedir@", r"${prefix}/include")
            content = content.replace(r"@PACKAGE_VERSION@", self.version)

            with open(pkgConfigFile, "wt") as f:
                f.write(content)

            # remove a dummy library and replace it with the real one
            utils.rmtree(self.installDir() / "lib/sqlcipher.lib")
            utils.copyFile(self.installDir() / "lib/libsqlcipher.lib", self.installDir() / "lib/sqlcipher.lib")

        return isInstalled


if CraftCore.compiler.isGCCLike():

    class Package(PackageAutotools):
        def __init__(self):
            PackageAutotools.__init__(self)

else:

    class Package(PackageMSVC):
        def __init__(self):
            PackageMSVC.__init__(self)
