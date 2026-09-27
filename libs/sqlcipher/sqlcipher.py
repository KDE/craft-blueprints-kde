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
import shutil

import info
import utils
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.MSBuildPackageBase import MSBuildPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.16.0"]:
            self.targets[ver] = f"https://github.com/sqlcipher/sqlcipher/archive/v{ver}.zip"
            self.archiveNames[ver] = f"sqlcipher-{ver}.zip"
            self.targetInstSrc[ver] = f"sqlcipher-{ver}"
            self.patchLevel[ver] = 1

        self.targetDigests["4.16.0"] = (["9f51a0960cc3cebaea62ff2bfa2ec3ef502b1be808d562d89cb876a18ed09d9c"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "4.16.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/openssl"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/tcl"] = None
        self.runtimeDependencies["libs/icu"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None

class PackageAutotools(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cFlags = "-DSQLITE_HAS_CODEC -DSQLITE_EXTRA_INIT=sqlcipher_extra_init -DSQLITE_EXTRA_SHUTDOWN=sqlcipher_extra_shutdown"
        self.subinfo.options.configure.noCacheFile = True
        self.subinfo.options.configure.noDataRootDir = True
        self.subinfo.options.configure.args += [
            "--with-tempstore=yes",
            "--dll-basename=libsqlcipher",
            "LDFLAGS=-lcrypto",
        ]
        if CraftCore.compiler.isMinGW():
            self.subinfo.options.make.supportsMultijob = False
            self.subinfo.options.configure.args += [f"CFLAGS='{cFlags}'"]
        else:
            self.subinfo.options.configure.args += [f"CFLAGS={cFlags}"]
        if CraftCore.compiler.isAndroid:
            craftRoot = str(CraftCore.standardDirs.craftRoot())
            candidates = [
                shutil.which("tclsh8.6", path=os.defpath),
                shutil.which("tclsh", path=os.defpath),
                "/usr/bin/tclsh8.6",
                "/bin/tclsh8.6",
                "/usr/bin/tclsh",
                "/bin/tclsh",
            ]
            tclsh = None
            for candidate in candidates:
                if not candidate:
                    continue
                if candidate.startswith(craftRoot):
                    continue
                if os.path.exists(candidate) and os.access(candidate, os.X_OK):
                    tclsh = candidate
                    break
            args = [
                "--disable-tcl",
                f"CPPFLAGS=-I{CraftCore.standardDirs.craftRoot() / 'include'}",
                f"LDFLAGS=-L{CraftCore.standardDirs.craftRoot() / 'lib'} -lcrypto -llog",
            ]
            if tclsh:
                args.append(f"TCLSH_CMD={tclsh}")
            self.subinfo.options.configure.args += args

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
        installDir = self.installDir()
        exeSuffix = ".exe" if CraftCore.compiler.isMinGW() else ""
        shellSrc = installDir / f"bin/sqlite3{exeSuffix}"
        if shellSrc.exists():
            utils.rmtree(installDir / f"bin/sqlcipher{exeSuffix}")
            utils.moveFile(shellSrc, installDir / f"bin/sqlcipher{exeSuffix}")

        staticLib = installDir / "lib/libsqlite3.a"
        if staticLib.exists():
            utils.rmtree(installDir / "lib/libsqlcipher.a")
            utils.moveFile(staticLib, installDir / "lib/libsqlcipher.a")

        includeDir = installDir / "include"
        if (includeDir / "sqlite3.h").exists():
            utils.createDir(includeDir / "sqlcipher")
            for header in ("sqlite3.h", "sqlite3ext.h"):
                headerFile = includeDir / header
                if headerFile.exists():
                    utils.moveFile(headerFile, includeDir / "sqlcipher" / header)

        pkgConfigDir = installDir / "lib/pkgconfig"
        sqlitePc = pkgConfigDir / "sqlite3.pc"
        sqlcipherPc = pkgConfigDir / "sqlcipher.pc"
        if sqlitePc.exists():
            with open(sqlitePc, "rt") as f:
                content = f.read()
            content = content.replace("Name: SQLite", "Name: SQLCipher")
            content = content.replace("-lsqlite3", "-lsqlcipher")
            content = content.replace("Cflags: -I${includedir}", "Cflags: -I${includedir}/sqlcipher")
            utils.rmtree(sqlitePc)
            with open(sqlcipherPc, "wt") as f:
                f.write(content)

        cmakes = [sqlcipherPc] if sqlcipherPc.exists() else []
        return self.patchInstallPrefix(cmakes, OsUtils.toMSysPath(self.subinfo.buildPrefix)[:-1], OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())[:-1])


class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def configure(self):
        self.enterSourceDir()
        fileName = "Makefile.msc"
        with open(fileName, "rt") as f:
            content = f.read()

        libDir = CraftCore.standardDirs.craftRoot() / "lib"
        includeLibs = f"LTLIBPATHS = $(LTLIBPATHS) /LIBPATH:{libDir}\n" "LTLIBS = $(LTLIBS) libssl.lib libcrypto.lib tcl86.lib\n"
        index = content.find("# If ICU support is enabled, add the linker options for it.")
        content = content[:index] + includeLibs + content[index:]

        with open(fileName, "wt") as f:
            f.write(content)
        return super().configure()

    def make(self):
        includeDir = CraftCore.standardDirs.craftRoot() / "include"
        libDir = CraftCore.standardDirs.craftRoot() / "lib"
        opts = "-DSQLITE_HAS_CODEC -DSQLITE_TEMP_STORE=2 -DSQLITE_EXTRA_INIT=sqlcipher_extra_init -DSQLITE_EXTRA_SHUTDOWN=sqlcipher_extra_shutdown " f"-I{includeDir}"
        macros = " ".join(
            [
                f'OPTS="{opts}"',
                "USE_CRT_DLL=1",  # stops segfaulting each time in qsqlcipher-test in KMyMoney with this, but is still unstable with core application
                "DYNAMIC_SHELL=1",
                "USE_ICU=1",
                f'ICUINCDIR="{includeDir}"',
                f'ICULIBDIR="{libDir}"',
                f'TCLINCDIR="{includeDir}"',
                f'TCLLIBDIR="{libDir}"',
            ]
        )
        return utils.system(f"nmake -f Makefile.msc {macros}")

    def install(self):
        isInstalled = super().install()
        if isInstalled:
            for src, dst in [
                ("bin/sqlite3.exe", "bin/sqlcipher.exe"),
                ("lib/sqlite3.lib", "lib/libsqlcipher.lib"),
                ("lib/libsqlite3.lib", "lib/libsqlcipher.lib"),
                ("bin/sqlite3.dll", "bin/libsqlcipher.dll"),
            ]:
                srcPath = self.installDir() / src
                if srcPath.exists():
                    utils.rmtree(self.installDir() / dst)
                    utils.moveFile(srcPath, self.installDir() / dst)

            # move sqlcipher headers to sqlcipher directory to not conflit with sqlite3
            includeDir = self.installDir() / "include"
            utils.moveFile(includeDir, self.installDir() / "sqlcipher")
            utils.createDir(includeDir)
            utils.moveFile(self.installDir() / "sqlcipher", includeDir / "sqlcipher")

            # allow finding sqlcipher library by pkgconfig module
            pkgConfigDir = self.installDir() / "lib/pkgconfig"
            pkgConfigFile = pkgConfigDir / "sqlcipher.pc"
            utils.createDir(pkgConfigDir)
            utils.copyFile(self.sourceDir() / "sqlite3.pc.in", pkgConfigFile)
            with open(pkgConfigFile, "rt") as f:
                content = f.read()
            content = content.replace(r"@prefix@", str(CraftCore.standardDirs.craftRoot()))
            content = content.replace(r"@exec_prefix@", r"${prefix}/bin")
            content = content.replace(r"@libdir@", r"${prefix}/lib")
            content = content.replace(r"@includedir@", r"${prefix}/include")
            content = content.replace(r"@PACKAGE_VERSION@", self.version)
            content = content.replace("Name: SQLite", "Name: SQLCipher")
            content = content.replace("-lsqlite3", "-lsqlcipher")
            content = content.replace("-I${includedir}", "-I${includedir}/sqlcipher")

            with open(pkgConfigFile, "wt") as f:
                f.write(content)

            # remove a dummy library and replace it with the real one
            utils.rmtree(self.installDir() / "lib/sqlcipher.lib")
            utils.copyFile(self.installDir() / "lib/libsqlcipher.lib", self.installDir() / "lib/sqlcipher.lib")

        return isInstalled


if CraftCore.compiler.isGCCLike():

    class Package(PackageAutotools):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

else:

    class Package(PackageMSVC):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
