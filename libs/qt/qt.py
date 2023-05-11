import info
from Package.VirtualPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("qtMajorVersion", "5")

    def setTargets(self):
        self.targets["latest"] = ""
        self.defaultTarget = "latest"


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
