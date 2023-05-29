# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["1.0.3"] = "http://downloads.xiph.org/releases/opus/opus-1.0.3.tar.gz"
        self.targets["1.1"] = "http://downloads.xiph.org/releases/opus/opus-1.1.tar.gz"
        for ver in ["1.3.1"]:
            self.targets[ver] = f"https://ftp.osuosl.org/pub/xiph/releases/opus/opus-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"opus-{ver}"

        if CraftCore.compiler.isMinGW():
            self.patchToApply["1.3.1"] = [
                ("libopus-1.3.1-20220324.diff", 1)
            ]  # https://github.com/msys2/MINGW-packages/blob/7c67d9c46554d10276b2017bcfd0290dfe24a1bf/mingw-w64-opus/PKGBUILD#L36

        self.targetDigests["1.0.3"] = "5781bd   d009943deb55a742ac99db20a0d4e89c1e"
        self.targetDigests["1.1"] = "35005f5549e2583f5770590135984dcfce6f3d58"
        self.targetDigests["1.3.1"] = (["65b58e1e25b2a114157014736a3d9dfeaad8d41be1c8179866f144a2fb44ff9d"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["1.0.3"] = "opus-1.0.3"
        self.targetInstSrc["1.1"] = "opus-1.1"

        self.description = "Opus codec library"
        self.defaultTarget = "1.3.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--disable-doc"]
        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.ldflags += " -lssp"
