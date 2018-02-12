# -*- coding: utf-8 -*-

# Copyright (C) 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import info
from Package.AutoToolsPackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["4.18"] = "https://www.aquamaniac.de/sites/download/download.php?package=01&release=206&file=01&dummy=gwenhywfar-4.18.0.tar.gz"
        self.targetDigests["4.18"] = (['6915bba42d8b7f0213cee186a944296e5e5e97cdbde5b539a924261af03086ca'], CraftHash.HashAlgorithm.SHA256)
        self.archiveNames["4.18"] = "gwenhywfar-4.18.0.tar.gz"
        self.targetInstSrc["4.18"] = "gwenhywfar-4.18.0"
        self.patchToApply["4.18"] = [("gwenhywfar-qt-detection.diff", 1)]
        self.defaultTarget = "4.18"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/xmlsec1"] = "default"
        self.runtimeDependencies["win32libs/gnutls"] = "default"
        self.runtimeDependencies["win32libs/gcrypt"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"

# 2018-02-11: compilation is successful if xmlmerge.exe gives any output in the console. For it to happen gnutls must be compiled with --enable-nls --enable-openssl-compatibility
class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = " --disable-static --enable-shared --disable-binreloc --with-guis=cpp qt5 "

    def configure(self):
        _, includedir = CraftCore.cache.getCommandOutput("qmake", "-query QT_INSTALL_HEADERS")
        includedir = self.shell.toNativePath(includedir.strip())
        widgetsdir = self.shell.toNativePath(os.path.join(includedir , "QtWidgets"))
        guidir = self.shell.toNativePath(os.path.join(includedir , "QtGui"))
        coredir = self.shell.toNativePath(os.path.join(includedir , "QtCore"))

        self.subinfo.options.configure.ldflags += '-lQt5Widgets -lQt5Gui -lQt5Core '
        self.subinfo.options.configure.cxxflags += f"-I{widgetsdir} -I{guidir} -I{coredir} -I{includedir} "
        return super().configure()


