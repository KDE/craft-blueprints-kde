# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        versions = ["2.9.2.1"]
        for ver in versions:
            self.targets[ver] = f"https://github.com/jgm/pandoc/releases/download/{ver}/pandoc-{ver}-macOS.zip"
        self.targetDigests["2.9.2.1"] = (['c4847f7a6e6a02a7d1b8dc17505896d8a6e4c2ee9e8b325e47a0468036675307'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.9.2.1"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        # On Mac, the files are neetly sorted into /bin and /share in the upstream zip, already. We just need to copy the whole thing, stripping the outer folder.
        dirs = os.listdir(self.workDir())
        if len(dirs) != 1:
            return False
        utils.copyDir(os.path.join(self.workDir(), dirs[0]), self.installDir())

        return True
