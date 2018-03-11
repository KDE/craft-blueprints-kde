# Copyright (C) 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import info

from Package.AutoToolsPackageBase import *
from Package.PackageBase import *
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.5.17"]:
            self.targets[ver] = "ftp://ftp.gnutls.org/gcrypt/gnutls/v3.5/gnutls-%s.tar.xz" % ver
            self.targetInstSrc[ver] = "gnutls-%s" % ver
        self.targetDigests['3.5.17'] = (['86b142afef587c118d63f72ccf307f3321dbc40357aae528202b65d913d20919'], CraftHash.HashAlgorithm.SHA256)
        self.description = "A library which provides a secure layer over a reliable transport layer"
        self.defaultTarget = "3.5.17"

    def setDependencies(self):
        self.runtimeDependencies["libs/gcrypt"] = "default"
        self.runtimeDependencies["libs/nettle"] = "default"
        self.runtimeDependencies["libs/libidn"] = "default"
        self.runtimeDependencies["autotools/libunistring"] = "default"
        self.runtimeDependencies["autotools/libtasn1"] = "default"
        self.runtimeDependencies["autotools/p11kit"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils-win/msys"] = "default"


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        # 2018-02-11: without --enable-openssl-compatibility xmlmerge.exe from gwenhywfar doesn't display any console output and in effect doesn't allow compilation of aqbanking
        # 2018-02-11: --enable-nls is probably needed on the same ground as above
        self.subinfo.options.configure.args = "--enable-shared --disable-static --with-zlib --enable-cxx --enable-nls --disable-gtk-doc --enable-local-libopts --enable-libopts-install --disable-tests --enable-openssl-compatibility "

if CraftCore.compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
