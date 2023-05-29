# -*- coding: utf-8 -*-
import info
from CraftCompiler import CraftCompiler


class subinfo(info.infoclass):
    def setTargets(self):
        arch = "i386"
        if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
            arch = "x86_64"
            self.targetDigests["2.17.1.1"] = (['bd5fb5c2ea78467ea6a6cffb043a98531a3b65f669aa16e8821d476fb67471be'], CraftHash.HashAlgorithm.SHA256)
        versions = ["2.17.1.1"]
        for ver in versions:
            self.targets[ver] = f"https://github.com/jgm/pandoc/releases/download/{ver}/pandoc-{ver}-windows-{arch}.zip"
        self.defaultTarget = "2.17.1.1"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False

        libdir = os.path.join(self.installDir(), "lib", "pandoc")
        dirs = os.listdir(self.installDir())
        if len(dirs) != 1:
            return False
        extractdir = os.path.join(self.installDir(), dirs[0])
        utils.moveFile(extractdir, libdir)
        utils.createShim(os.path.join(self.installDir(), "bin", "pandoc.exe"), os.path.join(libdir, "pandoc.exe"))

        return True
