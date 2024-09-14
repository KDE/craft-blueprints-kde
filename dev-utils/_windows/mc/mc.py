import os

import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["4.1.36"] = "https://www.siegward-jaekel.de/mc.zip"
        self.defaultTarget = "4.1.36"
        self.targetInstallPath["4.1.36"] = os.path.join("dev-utils", "bin")
        self.targetDigests["4.1.36"] = "cce65f21d52da1d21c6b60ca8defe7888a235b2f"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        f = open(self.installDir() / "mcedit.bat", "wb")
        f.write("mc -e %1")
        f.close()
        # mc is also a program in visual studio,
        # so make the real mc reachable from mcc too...
        utils.copyFile(self.installDir() / "mc.exe", self.installDir() / "mcc.exe")
        return True
