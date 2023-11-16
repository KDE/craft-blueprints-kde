import info
from CraftCompiler import CraftCompiler


class subinfo(info.infoclass):
    def setTargets(self):

        for ver in ["3.11.6"]:
            self.targets[ver] = f"https://www.python.org/ftp/python/{ver}/python-{ver}-embed-amd64.zip"
            self.targetInstallPath[ver] = "python"
        self.targetDigests["3.11.6"] = (["26d93c29cd627e7fc2085a7f08a88684c2831c3eed361d2be606ad89a023f194"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "3.11.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
