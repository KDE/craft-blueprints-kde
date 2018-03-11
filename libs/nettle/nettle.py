import info

from Package.AutoToolsPackageBase import *
from Package.PackageBase import *
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.4"]:
            self.targets[ver] = "http://www.lysator.liu.se/~nisse/archive/nettle-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "nettle-%s" % ver

        self.targetDigests['3.4'] = (['ae7a42df026550b85daca8389b6a60ba6313b0567f374392e54918588a411e94'], CraftHash.HashAlgorithm.SHA256)

        self.description = "A low-level cryptographic library"
        self.defaultTarget = "3.4"

    def setDependencies(self):
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils-win/msys"] = "default"
            self.runtimeDependencies["libs/libgmp"] = "default"
            self.runtimeDependencies["libs/openssl"] = "default"


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = " --enable-shared  --enable-public-key --disable-documentation"


if CraftCore.compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
