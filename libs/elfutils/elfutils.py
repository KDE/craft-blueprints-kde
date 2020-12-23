# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.181']:
            self.targets[ver] = 'https://sourceware.org/elfutils/ftp/%s/elfutils-%s.tar.bz2' % (ver, ver)
            self.targetInstSrc[ver] = "elfutils-" + ver

        self.patchLevel["0.181"] = 0
        self.targetDigests['0.181'] = (['d565541d5817f409dc89ebb1ee593366f69c371a1531308eeb67ff934b14a0fab0c9009fd7c23240efbaa1b4e04edac5c425e47d80e3e66ba03dcaf000afea36'], CraftHash.HashAlgorithm.SHA512)

        self.description = 'elfutils is a collection of utilities and libraries to read, create and modify ELF binary files, find and handle DWARF debug data, symbols, thread state and stacktraces for processes and core files on GNU/Linux.'
        self.defaultTarget = '0.181'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/libdwarf"] = None

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --disable-debuginfod "
        self.subinfo.options.configure.ldflags += " -lintl"
        self.platform = ""
