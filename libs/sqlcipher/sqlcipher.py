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
import stat

import info
import utils
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.MakeFilePackageBase import MakeFilePackageBase
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
        craftRoot = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())

        cFlags = (
            f"-DSQLITE_HAS_CODEC "
            f"-DSQLITE_EXTRA_INIT=sqlcipher_extra_init "
            f"-DSQLITE_EXTRA_SHUTDOWN=sqlcipher_extra_shutdown "
            f"-I{craftRoot}/include"
        )

        if CraftCore.compiler.isMinGW():
            ldFlags = f"-L{craftRoot}/lib -lcrypto -lm"
        elif CraftCore.compiler.isAndroid:
            ldFlags = f"-L{craftRoot}/lib -lcrypto -lm -llog"
        else:
            ldFlags = f"-L{craftRoot}/lib -lcrypto -lm -lpthread -ldl"

        self.subinfo.options.configure.supportsTargetOption = False
        self.subinfo.options.configure.supportsAutotoolsType = False

        self.subinfo.options.configure.noCacheFile = True
        self.subinfo.options.configure.noDataRootDir = True
        self.subinfo.options.configure.args += [
            "--with-tempstore=yes",
            "--dll-basename=libsqlcipher",
            f"CFLAGS={cFlags}",
            f"LDFLAGS={ldFlags}",
        ]

        if CraftCore.compiler.isMinGW():
            self.subinfo.options.make.supportsMultijob = False

        if CraftCore.compiler.isAndroid:
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
                if candidate.startswith(str(craftRoot)):
                    continue
                if os.path.exists(candidate) and os.access(candidate, os.X_OK):
                    tclsh = candidate
                    break

            args = [
                "--disable-tcl",
                f"CPPFLAGS=-I{craftRoot}/include",
            ]
            if tclsh:
                args.append(f"TCLSH_CMD={tclsh}")
            self.subinfo.options.configure.args += args

    @property
    def supportsTargetOption(self):
        return False

    def configure(self):
        def clean_arg(arg):
            is_args_obj = type(arg).__name__ == "Arguments"

            if is_args_obj and hasattr(arg, "get"):
                items = arg.get()
            elif isinstance(arg, (list, tuple)):
                items = arg
            elif isinstance(arg, str):
                return re.sub(r"\s*--target=\S+", "", arg)
            else:
                return arg

            cleaned_items = []
            for item in items:
                if isinstance(item, str):
                    item_clean = re.sub(r"--target=\S+", "", item).strip()
                    if item_clean:
                        cleaned_items.append(item_clean)
                else:
                    cleaned_items.append(item)

            if is_args_obj:
                try:
                    return arg.__class__(cleaned_items)
                except Exception:
                    return re.sub(r"\s*--target=\S+", "", str(arg))
            return type(arg)(cleaned_items)

        orig_system = utils.system

        def custom_system(cmd, **kwargs):
            return orig_system(clean_arg(cmd), **kwargs)

        utils.system = custom_system

        if hasattr(self, "shell") and self.shell:
            orig_execute = self.shell.execute

            def custom_execute(*args, **kwargs):
                cleaned_args = [clean_arg(a) for a in args]
                return orig_execute(*cleaned_args, **kwargs)
            self.shell.execute = custom_execute
        else:
            orig_execute = None

        try:
            isConfigured = super().configure()
        finally:
            utils.system = orig_system
            if orig_execute:
                self.shell.execute = orig_execute

        if isConfigured and CraftCore.compiler.isMinGW():
            Makefile = self.buildDir() / "Makefile"
            main_mk = self.sourceDir() / "main.mk"

            relativePath = ""
            if Makefile.exists():
                with open(Makefile, "rt") as f:
                    content = f.read()

                m = re.search(r"TCLLIBDIR\s*=\s*(?P<absolutePath>.*)", content)
                if m:
                    abs_path = m.group("absolutePath").strip()
                    if abs_path:
                        relativePath = os.path.relpath(abs_path, CraftCore.standardDirs.craftRoot())
                        relativePath = relativePath.replace("\\", "/")

            for mk_file in [Makefile, main_mk]:
                if mk_file.exists():
                    os.chmod(mk_file, stat.S_IWRITE | stat.S_IREAD)
                    with open(mk_file, "rt") as f:
                        mk_content = f.read()

                    mk_content = mk_content.replace(r"$(DESTDIR)$(bindir)", r"$(DESTDIR)/bin")
                    mk_content = mk_content.replace(r"$(DESTDIR)$(libdir)", r"$(DESTDIR)/lib")
                    mk_content = mk_content.replace(r"$(DESTDIR)$(includedir)", r"$(DESTDIR)/include/sqlcipher")
                    mk_content = mk_content.replace(r"$(DESTDIR)$(mandir)", r"$(DESTDIR)/share/man")
                    mk_content = mk_content.replace(r"$(DESTDIR)$(pkgconfigdir)", r"$(DESTDIR)/lib/pkgconfig")

                    if relativePath:
                        mk_content = mk_content.replace(r"$(DESTDIR)$(TCLLIBDIR)", r"$(DESTDIR)/" + relativePath)

                    with open(mk_file, "wt") as f:
                        f.write(mk_content)

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

        if CraftCore.compiler.isMinGW():
            libDir = installDir / "lib"
            dllImportLib = libDir / "libsqlcipher.dll.a"
            staticLibSqlCipher = libDir / "libsqlcipher.a"

            oldDllImport = libDir / "libsqlite3.dll.a"
            if oldDllImport.exists():
                utils.moveFile(oldDllImport, dllImportLib)

            if dllImportLib.exists() and not staticLibSqlCipher.exists():
                utils.copyFile(dllImportLib, staticLibSqlCipher)

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


class PackageMSVC(MakeFilePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def configure(self):
        self.enterSourceDir()
        fileName = self.sourceDir() / "Makefile.msc"
        if fileName.exists():
            with open(fileName, "rt") as f:
                content = f.read()

            content = content.replace("/NODEFAULTLIB:msvcrt", "")

            os.chmod(fileName, stat.S_IWRITE | stat.S_IREAD)
            with open(fileName, "wt") as f:
                f.write(content)
        return True

    def make(self):
        includeDir = CraftCore.standardDirs.craftRoot() / "include"
        libDir = CraftCore.standardDirs.craftRoot() / "lib"
        opts = (
            "-DSQLITE_HAS_CODEC "
            "-DSQLITE_TEMP_STORE=2 "
            "-DSQLITE_EXTRA_INIT=sqlcipher_extra_init "
            "-DSQLITE_EXTRA_SHUTDOWN=sqlcipher_extra_shutdown "
            "-DSQLCIPHER_CRYPTO_OPENSSL "
            f"-I{includeDir}"
        )

        macros = " ".join(
            [
                f'OPTS="{opts}"',
                "CODEC_TYPE=CODEC_TYPE_SQLCIPHER",
                "USE_CRT_DLL=1",
                "USE_DEF=1",
                "TCLSH=jimsh0.exe",
                "USE_ICU=1",
                f'ICUINCDIR="{includeDir}"',
                f'ICULIBDIR="{libDir}"',
                f'TCLINCDIR="{includeDir}"',
                f'TCLLIBDIR="{libDir}"',
                f'LTLIBPATHS="/LIBPATH:{libDir}"',
                'LTLIBS="libssl.lib libcrypto.lib tcl86.lib icuuc.lib icuin.lib"',
            ]
        )
        return utils.system(f"nmake -f Makefile.msc {macros}")

    def install(self):
        instDir = self.installDir()
        srcDir = self.sourceDir()

        utils.createDir(instDir / "bin")
        utils.createDir(instDir / "lib")
        utils.createDir(instDir / "include/sqlcipher")

        if (srcDir / "sqlite3.exe").exists():
            utils.copyFile(srcDir / "sqlite3.exe", instDir / "bin/sqlcipher.exe")
        if (srcDir / "sqlite3.dll").exists():
            utils.copyFile(srcDir / "sqlite3.dll", instDir / "bin/libsqlcipher.dll")
        if (srcDir / "sqlite3.lib").exists():
            utils.copyFile(srcDir / "sqlite3.lib", instDir / "lib/libsqlcipher.lib")
            utils.copyFile(srcDir / "sqlite3.lib", instDir / "lib/sqlcipher.lib")

        for h in ("sqlite3.h", "sqlite3ext.h"):
            if (srcDir / h).exists():
                utils.copyFile(srcDir / h, instDir / "include/sqlcipher" / h)
            elif (srcDir / "src" / h).exists():
                utils.copyFile(srcDir / "src" / h, instDir / "include/sqlcipher" / h)

        pkgConfigDir = instDir / "lib/pkgconfig"
        pkgConfigFile = pkgConfigDir / "sqlcipher.pc"
        utils.createDir(pkgConfigDir)

        pcIn = srcDir / "sqlite3.pc.in"
        if pcIn.exists():
            utils.copyFile(pcIn, pkgConfigFile)
            with open(pkgConfigFile, "rt") as f:
                content = f.read()
            craftRootUnix = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
            content = content.replace(r"@prefix@", craftRootUnix)
            content = content.replace(r"@exec_prefix@", r"${prefix}/bin")
            content = content.replace(r"@libdir@", r"${prefix}/lib")
            content = content.replace(r"@includedir@", r"${prefix}/include")
            content = content.replace(r"@PACKAGE_VERSION@", self.version)
            content = content.replace("Name: SQLite", "Name: SQLCipher")
            content = content.replace("-lsqlite3", "-lsqlcipher")
            content = content.replace("-I${includedir}", "-I${includedir}/sqlcipher")

            with open(pkgConfigFile, "wt") as f:
                f.write(content)

        return True


if CraftCore.compiler.isGCCLike():

    class Package(PackageAutotools):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

else:

    class Package(PackageMSVC):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
