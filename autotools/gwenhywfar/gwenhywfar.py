# -*- coding: utf-8 -*-

# Copyright (C) 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import re
import info
from Package.AutoToolsPackageBase import *
from CraftOS.osutils import OsUtils

class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["4.19"] = "https://www.aquamaniac.de/sites/download/download.php?package=01&release=207&file=01&dummy=gwenhywfar-4.19.0.tar.gz"
        self.targetDigests["4.19"] = (['c54a9a162dc63ab69e4d3fc946aae92b929383ca60a2690b539adcdc58de9495'], CraftHash.HashAlgorithm.SHA256)
        self.archiveNames["4.19"] = "gwenhywfar-4.19.0.tar.gz"
        self.targetInstSrc["4.19"] = "gwenhywfar-4.19.0"
        self.patchToApply["4.19"] = [("gwenhywfar-4.19.0-20180218.diff", 1)]
        # self.patchToApply["4.19"] = [("gwenhywfar-qt-detection.diff", 1)]
        self.defaultTarget = "4.19"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/xmlsec1"] = "default"
        self.runtimeDependencies["libs/gnutls"] = "default"
        self.runtimeDependencies["libs/gcrypt"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"

# 2018-02-11: compilation is successful if xmlmerge.exe gives any output in the console. For it to happen gnutls must be compiled with --enable-nls --enable-openssl-compatibility
class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared --disable-binreloc --with-guis='qt5 cpp'"

    def configure(self):
        _, includedir = CraftCore.cache.getCommandOutput("qmake", "-query QT_INSTALL_HEADERS")
        includedir = self.shell.toNativePath(includedir.strip())
        widgetsdir = self.shell.toNativePath(os.path.join(includedir , "QtWidgets"))
        guidir = self.shell.toNativePath(os.path.join(includedir , "QtGui"))
        coredir = self.shell.toNativePath(os.path.join(includedir , "QtCore"))

        self.subinfo.options.configure.cxxflags += f"-I{widgetsdir} -I{guidir} -I{coredir} -I{includedir} "
        return super().configure()

    def install(self):
        if OsUtils.isWin():
            cmakes = [ os.path.join(self.buildDir(), "gui", "cpp", "gwengui-cpp-config.cmake"),
                    os.path.join(self.buildDir(), "gui", "qt5", "gwengui-qt5-config.cmake"),
                    os.path.join(self.buildDir(), "gwenhywfar-config.cmake")
                    ]
            for cmake in cmakes:
                f = open(cmake, "r+")
                cmakeFileContents = f.readlines()
                for i in range(len(cmakeFileContents)):
                    m = re.search('set_and_check\(prefix "(?P<root>[^"]*)"\)', cmakeFileContents[i])
                    if m is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace(m.group('root'), CraftStandardDirs.craftRoot()[:-1])

                    m2 = re.search("libgwenhywfar.so.(?P<number>[\d]*)", cmakeFileContents[i])
                    if m2 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace("lib/" + m2.group(0), "bin/libgwenhywfar-" + m2.group('number') +".dll")

                    m3 = re.search("libgwengui-cpp.so", cmakeFileContents[i])
                    if m3 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace("lib/libgwengui-cpp.so", "bin/libgwengui-cpp-0.dll")

                    m4 = re.search("libgwengui-qt5.so", cmakeFileContents[i])
                    if m4 is not None:
                        cmakeFileContents[i] = cmakeFileContents[i].replace("lib/libgwengui-qt5.so", "lib/libgwengui-qt5.a")

                f.seek(0)
                f.write(''.join(cmakeFileContents))
                f.close()
        return AutoToolsPackageBase.install(self)
