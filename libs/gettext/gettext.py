# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *
from Package.MSBuildPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ["0.21", "0.21.1"]:
            self.targets[ver] = "http://ftp.gnu.org/pub/gnu/gettext/gettext-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "gettext-%s" % ver
        self.targetDigests["0.21"] = (["c77d0da3102aec9c07f43671e60611ebff89a996ef159497ce8e59d075786b12"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.21.1"] = (["e8c3650e1d8cee875c4f355642382c1df83058bd5a11ee8555c0cf276d646d45"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["0.21"] = [
            ("gettext-0.21-add-missing-ruby.diff", 1),
            (
                "d1836dbbd6a90b4c0ab79bc5292c023f08b49511.patch",
                1,
            ),  # https://git.savannah.gnu.org/gitweb/?p=gettext.git;a=commitdiff;h=d1836dbbd6a90b4c0ab79bc5292c023f08b49511
            ("gettext-0.21.1-20230603.diff", 1),  # fix windows search path
            # https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/gettext/parallel-gettext-tools.patch
            ("parallel-gettext-tools.patch", 1),
        ]

        self.patchToApply["0.21.1"] = [
            ("gettext-0.21.1-20230603.diff", 1),  # fix windows search path
            # https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/gettext/parallel-gettext-tools.patch
            ("parallel-gettext-tools.patch", 1),
        ]
        if CraftCore.compiler.isMinGW():
            self.patchToApply["0.21"] += [
                ("0011-fix-interference-between-libintl-boost-header-files.patch", 1)
            ]  # https://github.com/msys2/MINGW-packages/blob/master/mingw-w64-gettext/0011-fix-interference-between-libintl-boost-header-files.patch
            self.patchToApply["0.21.1"] += [
                ("0011-fix-interference-between-libintl-boost-header-files.patch", 1)
            ]  # https://github.com/msys2/MINGW-packages/blob/master/mingw-w64-gettext/0011-fix-interference-between-libintl-boost-header-files.patch
            self.patchLevel["0.21"] = 2

        self.description = "GNU internationalization (i18n)"
        # 0.21.1 fails on Windows
        # libgettextsrc_la-write-catalog.obj : error LNK2019: unresolved external symbol close_used_without_requesting_gnulib_module_close referenced in function msgdomain_list_print
        # .libs\gettextsrc-0-21-1.dll : fatal error LNK1120: 1 unresolved external
        self.defaultTarget = "0.21"

    def setDependencies(self):
        self.buildDependencies["dev-utils/automake"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/iconv"] = None
        if not CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/libxml2"] = None
        else:
            self.buildDependencies["dev-utils/msys"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.shell.useMSVCCompatEnv = True
        self.subinfo.options.configure.args += [
            "--disable-static",
            "--enable-shared",
            "--disable-acl",
            "--disable-java",
            "--disable-native-java",
            "--enable-nls",
            "--enable-c++",
            "--enable-relocatable",
            "--with-included-gettext",
            "--with-included-glib",
            "--with-included-regex",
            "--with-gettext-tools",
            "--without-cvs",
            "--without-emacs",
            "--without-git",
            "--disable-dependency-tracking",
        ]

        if CraftCore.compiler.isMSVC():
            # workaround for "'C:C:/CraftRoot/msys/CraftRoot/build/_/527d4567/gettext-0.21/gettext-runtime/libasprintf/autosprintf.cc'"
            self.subinfo.options.useShadowBuild = False
            # https://github.com/microsoft/vcpkg/blob/c6a4ed75f03a7485cf6fc91794809cd73f8f5aeb/ports/gettext/portfile.cmake#L49
            self.subinfo.options.configure.args += [
                "--with-included-libxml",
                # they are not properly detected, and when gnulib tries to define them they clash with the intrinsic definition
                # memset.c(23): error C2169: 'memset': intrinsic function, cannot be defined
                "ac_cv_func_wcslen=yes",
                "ac_cv_func_memmove=yes",
                "ac_cv_func_memset=yes",
            ]
        else:
            self.subinfo.options.configure.args += ["--without-included-libxml"]

    def postInstall(self):
        return self.patchInstallPrefix(
            [
                os.path.join(self.installDir(), "bin", "autopoint"),
                os.path.join(self.installDir(), "bin", "gettextize"),
                os.path.join(self.installDir(), "lib", "gettext", "user-email"),
            ],
            self.subinfo.buildPrefix,
            CraftCore.standardDirs.craftRoot(),
        )
