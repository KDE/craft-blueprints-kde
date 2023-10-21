# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *
from Package.MSBuildPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        # On Android we use libintl-lite instead
        # (however gettext added Adnroid support recently so maybe we should look into switching to it?)
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ["0.21", "0.22.3"]:
            self.targets[ver] = "https://ftp.gnu.org/pub/gnu/gettext/gettext-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "gettext-%s" % ver
        self.targetDigests["0.21"] = (["c77d0da3102aec9c07f43671e60611ebff89a996ef159497ce8e59d075786b12"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.22.3"] = (["839a260b2314ba66274dae7d245ec19fce190a3aa67869bf31354cb558df42c7"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["0.21"] = [
            ("gettext-0.21-add-missing-ruby.diff", 1),
            (
                "d1836dbbd6a90b4c0ab79bc5292c023f08b49511.patch",
                1,
            ),  # https://git.savannah.gnu.org/gitweb/?p=gettext.git;a=commitdiff;h=d1836dbbd6a90b4c0ab79bc5292c023f08b49511
        ]

        if CraftCore.compiler.isMinGW():
            self.patchToApply["0.21"] += [
                ("0011-fix-interference-between-libintl-boost-header-files.patch", 1)
            ]  # https://github.com/msys2/MINGW-packages/blob/master/mingw-w64-gettext/0011-fix-interference-between-libintl-boost-header-files.patch
            self.patchLevel["0.21"] = 2

        self.description = "GNU internationalization (i18n)"
        self.defaultTarget = "0.22.3"

    def setDependencies(self):
        self.buildDependencies["dev-utils/automake"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.buildDependencies["dev-utils/msys"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.shell.useMSVCCompatEnv = True
        self.subinfo.options.configure.args += [
            "--disable-static",
            "--enable-shared",
            "--disable-java",
            "--disable-native-java",
            "--enable-nls",
            "--enable-c++",
            "--with-included-gettext",
            "--with-included-glib",
            "--with-included-regex",
            "--with-gettext-tools",
        ]

        if CraftCore.compiler.isMSVC():
            # workaround for "'C:C:/CraftRoot/msys/CraftRoot/build/_/527d4567/gettext-0.21/gettext-runtime/libasprintf/autosprintf.cc'"
            self.subinfo.options.useShadowBuild = False
            # https://github.com/microsoft/vcpkg/blob/c6a4ed75f03a7485cf6fc91794809cd73f8f5aeb/ports/gettext/portfile.cmake#L49
            self.subinfo.options.configure.args += [
                "ac_cv_func_wcslen=yes",
                "ac_cv_func_memmove=yes"
                # The following are required for a full gettext built (libintl and tools).
                "gl_cv_func_printf_directive_n=no",  # segfaults otherwise with popup window
                "ac_cv_func_memset=yes",  # not detected in release builds
                "ac_cv_header_pthread_h=no",
                "ac_cv_header_dirent_h=no",
                "ac_cv_header_getopt_h=no",
            ]

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
