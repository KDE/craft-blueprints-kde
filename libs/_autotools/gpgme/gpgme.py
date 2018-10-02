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
import re
import CraftCore


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["1.9.0", "1.11.1"]:
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/gpgme/gpgme-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"gpgme-{ver}"

        self.targetDigests["1.9.0"] = (["1b29fedb8bfad775e70eafac5b0590621683b2d9869db994568e6401f4034ceb"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.11.1"] = (["2d1b111774d2e3dd26dcd7c251819ce4ef774ec5e566251eb9308fa7542fbd6f"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.9.0"] = [("gpgme-1.9.0-20170801.diff", 1)]
        self.patchToApply["1.11.1"] = [("gpgme-1.1.11-20170801.diff", 1),
                                       ("qt Respect --disable-gpg-test for tests.patch", 1),
                                       ("gpgme-1.11.1-20180820.diff", 1),# disable the documentation (crashes on x86)
                                       ("gpgme-1.11.1-20180920.diff", 1),# fix qgpgme config
                                       ]
        if CraftCore.compiler.isWindows:
            self.patchToApply["1.11.1"] += [("gpgme-1.1.11-20180620.diff", 1)]

        self.patchLevel["1.11.1"] = 4

    def registerOptions(self):
        self.options.dynamic.registerOption("enableCPP", True)

        self.description = "GnuPG cryptography support library (runtime)"
        self.defaultTarget = "1.11.1"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/assuan2"] = None
        if self.options.dynamic.enableCPP:
            self.runtimeDependencies["libs/qt5/qtbase"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        if not self.subinfo.options.dynamic.enableCPP:
            self.subinfo.options.configure.args = "--enable-languages=no"
        else:
            self.subinfo.options.configure.args = "--enable-languages=cpp,qt"
        self.subinfo.options.configure.args += " --disable-gpg-test"

    def configure(self):
        if self.subinfo.options.dynamic.enableCPP:
            # The configure script does not honnor the env var is PKG_CONFIG is not installed / env var not set
            # This is problematic especially on macOS, let manually fill the env var to make configure happy finding Qt
            PKG_CONFIG = ":"
            # Gpgme rely on pkg-config to discover Qt, but pkg config files are not shipped / generated...
            # So we need to help it to discover Qt
            QT_BINS = CraftCore.cache.getCommandOutput("qmake", "-query QT_INSTALL_BINS")[1].strip()
            QT_LIBS = CraftCore.cache.getCommandOutput("qmake", "-query QT_INSTALL_LIBS")[1].strip()
            QT_INCLUDES = CraftCore.cache.getCommandOutput("qmake", "-query QT_INSTALL_HEADERS")[1].strip()
            MOC = f"{QT_BINS}/moc"
            if CraftCore.compiler.isMacOS:
                GPGME_QT_CFLAGS = f"-F{QT_LIBS} -I{QT_LIBS}/QtCore.framework/Headers -DQT_NO_DEBUG -DQT_CORE_LIB"
                GPGME_QT_LIBS = f"-F{QT_LIBS} -framework QtCore"
                GPGME_QTTEST_CFLAGS = f"-F{QT_LIBS} -I{QT_LIBS}/QtTest.framework/Headers -DQT_NO_DEBUG -DQT_TEST_LIB"
                GPGME_QTTEST_LIBS = f"-F{QT_LIBS} -framework QtTest"
            else:
                if CraftCore.compiler.isWindows and self.buildType() == "Debug":
                    debugSuffix = "d"
                else:
                    debugSuffix = ""
                GPGME_QT_CFLAGS = f"-I{QT_INCLUDES} -I{QT_INCLUDES}/QtCore -DQT_NO_DEBUG -DQT_CORE_LIB"
                GPGME_QT_LIBS = f"-L{QT_LIBS} -lQt5Core{debugSuffix}"
                GPGME_QTTEST_CFLAGS = f"-I{QT_INCLUDES} -I{QT_INCLUDES}/QtTest -DQT_NO_DEBUG -DQT_TEST_LIB"
                GPGME_QTTEST_LIBS = f"-L{QT_LIBS} -lQt5Test{debugSuffix}"
            self.subinfo.options.configure.args += (f" PKG_CONFIG='{PKG_CONFIG}'"
                f" MOC='{MOC}'"
                f" GPGME_QT_CFLAGS='{GPGME_QT_CFLAGS}'"
                f" GPGME_QT_LIBS='{GPGME_QT_LIBS}'"
                f" GPGME_QTTEST_CFLAGS='{GPGME_QTTEST_CFLAGS}'"
                f" GPGME_QTTEST_LIBS='{GPGME_QTTEST_LIBS}'")
        return AutoToolsPackageBase.configure(self)

    def postInstall(self):
        if not self.copyToMsvcImportLib():
            return False
        if self.subinfo.options.dynamic.enableCPP:
            cmakes = [ os.path.join(self.installDir(), "lib" , "cmake", "Gpgmepp", "GpgmeppConfig.cmake"),
                        os.path.join(self.installDir(), "lib" , "cmake", "QGpgme", "QGpgmeConfig.cmake") ]
        else:
            cmakes = []
        return (self.patchInstallPrefix(cmakes,
                                        OsUtils.toMSysPath(self.subinfo.buildPrefix),
                                        OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())) and
                self.patchInstallPrefix(cmakes,
                                        OsUtils.toUnixPath(self.subinfo.buildPrefix),
                                        OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())) and
                self.patchInstallPrefix([os.path.join(self.installDir(), "bin", "gpgme-config")],
                                        OsUtils.toMSysPath(self.subinfo.buildPrefix),
                                        OsUtils.toMSysPath(CraftCore.standardDirs.craftRoot())))
