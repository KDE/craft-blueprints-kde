import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["2.2"] = "http://www.dependencywalker.com/depends22_x64.zip"
        self.targetInstallPath["2.2"] = "dev-utils/bin"
        self.defaultTarget = "2.2"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
