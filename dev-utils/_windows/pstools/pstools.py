import os

import info
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["2.44"] = "http://download.sysinternals.com/Files/PsTools.zip"
        self.defaultTarget = "2.44"
        # the zip file does not have a bin dir, so we have to create it
        # This attribute is in prelimary state
        self.targetInstallPath["2.44"] = os.path.join("dev-utils", "bin")


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
