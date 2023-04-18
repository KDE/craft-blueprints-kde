# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Linux

    def setTargets(self):
        for ver in ["0.181", "0.185", "0.188"]:
            self.targets[ver] = "https://sourceware.org/elfutils/ftp/%s/elfutils-%s.tar.bz2" % (ver, ver)
            self.targetInstSrc[ver] = "elfutils-" + ver
            self.patchLevel[ver] = 0

        self.targetDigests["0.181"] = (
            ["d565541d5817f409dc89ebb1ee593366f69c371a1531308eeb67ff934b14a0fab0c9009fd7c23240efbaa1b4e04edac5c425e47d80e3e66ba03dcaf000afea36"],
            CraftHash.HashAlgorithm.SHA512,
        )
        self.targetDigests["0.185"] = (
            ["34de0de1355b11740e036e0fc64f2fc063587c8eb121b19216ee5548d3f0f268d8fc3995176c47190466b9d881007cfa11a9d01e9a50e38af6119492bf8bb47f"],
            CraftHash.HashAlgorithm.SHA512,
        )
        self.targetDigests["0.188"] = (["fb8b0e8d0802005b9a309c60c1d8de32dd2951b56f0c3a3cb56d21ce01595dff"], CraftHash.HashAlgorithm.SHA256)

        self.description = "elfutils is a collection of utilities and libraries to read, create and modify ELF binary files, find and handle DWARF debug data, symbols, thread state and stacktraces for processes and core files on GNU/Linux."
        self.defaultTarget = "0.188"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/libzstd"] = None
        self.runtimeDependencies["libs/libdwarf"] = None
        self.runtimeDependencies["libs/libcurl"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--disable-debuginfod", "--enable-install-elfh"]
        self.subinfo.options.configure.ldflags += " -lintl"
