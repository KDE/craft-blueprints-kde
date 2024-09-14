import os

import info
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = "https://download.sysinternals.com/files/ProcessMonitor.zip"
        self.defaultTarget = "latest"
        self.targetInstallPath["latest"] = os.path.join("dev-utils", "bin")


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
