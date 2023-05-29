import stat
from pathlib import Path

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1-alpha-20220822-1"]:
            self.targets[ver] = "https://github.com/linuxdeploy/linuxdeploy/releases/download/1-alpha-20220822-1/linuxdeploy-x86_64.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"
            self.defaultTarget = ver
        self.targetDigests["1-alpha-20220822-1"] = (["fb9183b0cac3985829f8dbcdcaa2bc0fa4bb7db0e1a7215e23f52f31088c993d"], CraftHash.HashAlgorithm.SHA256)
        self.description = "AppDir creation and maintenance tool. Featuring flexible plugin system."
        self.webpage = "https://github.com/linuxdeploy/linuxdeploy"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/linuxdeploy-plugin-qt"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)
