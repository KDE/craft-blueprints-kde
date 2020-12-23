# -*- coding: utf-8 -*-
import info
from Package.MSBuildPackageBase import *
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.19.8.1', '0.21']:
            self.targets[ver] = 'http://ftp.gnu.org/pub/gnu/gettext/gettext-%s.tar.gz' % ver
            self.targetInstSrc[ver] = "gettext-%s" % ver
        self.patchLevel['0.19.8.1'] = 1
        self.targetDigests['0.19.8.1'] = (['ff942af0e438ced4a8b0ea4b0b6e0d6d657157c5e2364de57baa279c1c125c43'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['0.21'] = (['c77d0da3102aec9c07f43671e60611ebff89a996ef159497ce8e59d075786b12'], CraftHash.HashAlgorithm.SHA256)

        #patch based on https://github.com/fanc999/gtk-msvc-projects/tree/master/gettext/0.19.8.1
        self.patchToApply['0.19.8.1'] = [("gettext-0.19.8.1-gtk-msvc-projects.diff", 1),
                                        ("0001-gettext-tools-gnulib-lib-xalloc.h-Fix-function-signa.patch", 1),
                                        ("0001-gettext-tools-src-Fix-linking.patch", 1),
                                        ("0001-gettext-tools-src-x-lua.c-Fix-on-pre-C99.patch", 1),
                                        ("0001-ostream.h-styled-ostream.h-Fix-linking.patch", 1),
                                        ("0001-printf-parse.c-Fix-build-on-Visual-Studio-2008.patch", 1),
                                        ("0001-tools-Fix-gnulib-lib-uniname-uniname.c-on-pre-C99.patch", 1)]

        #https://raw.githubusercontent.com/Alexpux/MINGW-packages/35567f5ba0f3bf2db06ea321090432cdafe024af/mingw-w64-gettext/09-asm-underscore-mingw.patch
        self.patchToApply['0.19.8.1'] += [("09-asm-underscore-mingw.patch", 1)]

        if CraftCore.compiler.isWindows:
            self.patchToApply['0.19.8.1'] += [("gettext-0.19.8.1-20180607.diff", 2)]
        elif CraftCore.compiler.isMacOS:
            self.patchToApply['0.19.8.1'] += [("0001-moopp-sed-extended-regexp.patch", 1)]

        self.description = "GNU internationalization (i18n)"
        self.defaultTarget = '0.19.8.1'
        if CraftCore.compiler.isFreeBSD:
            self.defaultTarget = '0.21'

    def setDependencies(self):
        self.buildDependencies["dev-utils/automake"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        if CraftCore.compiler.isGCCLike():
            self.buildDependencies["dev-utils/msys"] = None


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared --disable-java --disable-native-java --enable-nls --enable-c++ --with-included-gettext --with-included-glib --with-included-regex --with-gettext-tools"

    def postInstall(self):
        return self.patchInstallPrefix([os.path.join(self.installDir(), "bin", "autopoint"),
                                        os.path.join(self.installDir(), "bin", "gettextize"),
                                        os.path.join(self.installDir(), "lib", "gettext", "user-email")],
                                       self.subinfo.buildPrefix,
                                       CraftCore.standardDirs.craftRoot())

class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)
        self.gettextBuildDir = os.path.join(self.sourceDir(), "win32", "vs15")
        self.subinfo.options.configure.args = "/p:UseEnv=true"
        self.subinfo.options.configure.projectFile = os.path.join(self.gettextBuildDir, "gettext.sln")

    def install(self):
        if not MSBuildPackageBase.install(self, installHeaders=False,
                                          buildDirs=[self.gettextBuildDir]):
            return True
        return (utils.copyFile(os.path.join(self.sourceDir(), "gettext-runtime", "intl", "msvc", "libintl.h"),
                               os.path.join(self.installDir(), "include", "libintl.h")) and
                utils.copyFile(os.path.join(self.sourceDir(), "gettext-runtime", "libasprintf", "msvc", "autosprintf.h"),
                               os.path.join(self.installDir(), "include", "autosprintf.h")))

if CraftCore.compiler.isGCCLike():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(PackageMSVC):
        def __init__(self):
            PackageMSVC.__init__(self)
