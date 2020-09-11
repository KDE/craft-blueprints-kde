# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets(self):
        arch = "i386"
        if CraftCore.compiler.isX64():
            arch = "x86_64"
        versions = ["2.9.2.1"]
        for ver in versions:
            self.targets[ver] = f"https://github.com/jgm/pandoc/releases/download/{ver}/pandoc-{ver}-windows-{arch}.zip"
        self.targetDigestsX64["2.9.2.1"] = (['223f7ef1dd926394ee57b6b5893484e51100be8527bd96eec26e284774863084'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.9.2.1"

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False

        libdir = os.path.join(self.installDir(), "lib", "pandoc")
        dirs = os.listdir(self.workDir())
        if len(dirs) != 1:
            return False
        utils.moveFile(dirs[0], libdir)
        utils.createShim(os.path.join(self.installDir(), "bin", "pandoc.exe"), os.path.join(libdir, "pandoc.exe"))

        return True
