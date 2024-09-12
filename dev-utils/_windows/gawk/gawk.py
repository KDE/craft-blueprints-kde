import info
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["3.1.6-1"] = "https://downloads.sourceforge.net/sourceforge/gnuwin32/gawk-3.1.6-1-bin.zip"
        self.targetInstallPath["3.1.6-1"] = "dev-utils"
        self.targetDigests["3.1.6-1"] = "bda507655eb3d15059d8a55a0daf6d697a15f632"
        self.defaultTarget = "3.1.6-1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
