import info
from Package.VirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.defaultTarget = "latest"


class Package(VirtualPackageBase):
    def __init__(self):
        super().__init__()
