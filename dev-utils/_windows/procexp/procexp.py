import os

import info
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["16.26"]:
            self.targets[ver] = "http://download.sysinternals.com/files/ProcessExplorer.zip"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")
        self.defaultTarget = "16.26"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
