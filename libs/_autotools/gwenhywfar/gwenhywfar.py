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

import re

import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["5.8.1"] = "https://www.aquamaniac.de/rdm/attachments/download/402/gwenhywfar-5.8.1.tar.gz"
        self.targetDigests["5.8.1"] = (["05397618b9cae0197a181835f67e19ba09652cf30e2c9d1fbb98f3f34dbf4e1f"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["5.8.1"] = "gwenhywfar-5.8.1"
        self.patchToApply["5.8.1"] = [("gwenhywfar-5.8.1-20211230.diff", 0)]
        if CraftCore.compiler.isMinGW():
            self.patchToApply["5.8.1"] += [("gwenhywfar-4.19.0-20180218.diff", 1)]
        self.patchLevel["5.8.1"] = 3

        self.targets["5.10.1"] = "https://www.aquamaniac.de/rdm/attachments/465/gwenhywfar-5.10.1.tar.gz"
        self.targetDigests["5.10.1"] = (["a2f60a9dde5da27e57e0e5ef5f8931f495c1d541ad90a841e2b6231565547160"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["5.10.1"] = "gwenhywfar-5.10.1"
        self.defaultTarget = "5.10.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/xmlsec1"] = None
        self.runtimeDependencies["libs/gnutls"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


# 2018-02-11: compilation is successful if xmlmerge.exe gives any output in the console. For it to happen gnutls must be compiled with --enable-nls --enable-openssl-compatibility
class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared --with-guis='qt5 cpp'"
        # For appImage builds the --enable-local-install is needed so that
        # the appImage is searched for gwenhywfar plugins
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += " --enable-local-install --enable-binreloc"

        # Disable autoreconf. Otherwise following errors prevent configuring:
        # configure.ac:618: warning: macro 'AM_PATH_LIBGCRYPT' not found in library
        # configure.ac:633: warning: macro 'AM_PATH_GPG_ERROR' not found in library
        self.subinfo.options.configure.autoreconf = False

    def configure(self):
        if CraftCore.compiler.isMinGW():
            _, includedir = CraftCore.cache.getCommandOutput("qmake", "-query QT_INSTALL_HEADERS")
            includedir = self.shell.toNativePath(includedir.strip())
            widgetsdir = self.shell.toNativePath(os.path.join(includedir, "QtWidgets"))
            guidir = self.shell.toNativePath(os.path.join(includedir, "QtGui"))
            coredir = self.shell.toNativePath(os.path.join(includedir, "QtCore"))

            self.subinfo.options.configure.cxxflags += f"-I{widgetsdir} -I{guidir} -I{coredir} -I{includedir} "
        return super().configure()

    def postInstall(self):
        versionWithoutPatch = ".".join(self.subinfo.buildTarget.split(".")[0:2])
        cmakes = [
            os.path.join(self.installDir(), "lib", "cmake", f"gwengui-cpp-{versionWithoutPatch}", "gwengui-cpp-config.cmake"),
            os.path.join(self.installDir(), "lib", "cmake", f"gwengui-qt5-{versionWithoutPatch}", "gwengui-qt5-config.cmake"),
            os.path.join(self.installDir(), "lib", "cmake", f"gwenhywfar-{versionWithoutPatch}", "gwenhywfar-config.cmake"),
        ]
        for cmake in cmakes:
            with open(cmake, "rt") as f:
                cmakeFileContents = f.readlines()

            for i in range(len(cmakeFileContents)):
                if CraftCore.compiler.isMinGW():
                    m = re.search('set_and_check\(prefix "(?P<root>[^"]*)"\)', cmakeFileContents[i])
                    if m is not None:
                        # somehow this doesn't produce forward slash path in CI
                        # craftRoot = OsUtils.toUnixPath(CraftStandardDirs.craftRoot())
                        craftRoot = CraftStandardDirs.craftRoot()
                        craftRoot = craftRoot.replace("\\", "/")
                        if craftRoot.endswith("/"):
                            craftRoot = craftRoot[:-1]
                        cmakeFileContents[i] = cmakeFileContents[i].replace(m.group("root"), craftRoot)

                    m2 = re.search("libgwenhywfar.so.(?P<number>[\d]*)", cmakeFileContents[i])
                    if m2 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace("lib/" + m2.group(0), "bin/libgwenhywfar-" + m2.group("number") + ".dll")

                    m3 = re.search("libgwengui-cpp.so", cmakeFileContents[i])
                    if m3 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace("lib/libgwengui-cpp.so", "bin/libgwengui-cpp-0.dll")

                    m4 = re.search("libgwengui-qt5.so", cmakeFileContents[i])
                    if m4 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace("lib/libgwengui-qt5.so", "lib/libgwengui-qt5.a")
                elif CraftCore.compiler.isMacOS:
                    m2 = re.search("libgwenhywfar.so.(?P<number>[\d]*)", cmakeFileContents[i])
                    if m2 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace(m2.group(0), "libgwenhywfar." + m2.group("number") + ".dylib")

                    m3 = re.search("libgwengui-cpp.so", cmakeFileContents[i])
                    if m3 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace("libgwengui-cpp.so", "libgwengui-cpp.dylib")

                    m4 = re.search("libgwengui-qt5.so", cmakeFileContents[i])
                    if m4 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace("libgwengui-qt5.so", "libgwengui-qt5.dylib")

                with open(cmake, "wt") as f:
                    f.write("".join(cmakeFileContents))

        return AutoToolsPackageBase.postInstall(self)
