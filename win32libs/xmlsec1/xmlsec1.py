# -*- coding: utf-8 -*-

# Copyright (C) 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["1.2.25"] = "https://www.aleksey.com/xmlsec/download/xmlsec1-1.2.25.tar.gz"
        self.targetDigests["1.2.25"] = (['967ca83edf25ccb5b48a3c4a09ad3405a63365576503bf34290a42de1b92fcd2'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["1.2.25"] = "xmlsec1-1.2.25"
        self.defaultTarget = "1.2.25"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/libxml2"] = "default"
        self.runtimeDependencies["win32libs/libxslt"] = "default"
        self.runtimeDependencies["win32libs/libidn"] = "default"
        self.runtimeDependencies["win32libs/gnutls"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *

class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = " --enable-shared --disable-static --without-openssl --disable-crypto-dl"
        self.subinfo.options.configure.ldflags += '-lgcrypt '


if CraftCore.compiler.isGCCLike:
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
