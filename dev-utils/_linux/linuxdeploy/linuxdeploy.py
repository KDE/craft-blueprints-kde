import stat
from pathlib import Path

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1-alpha-20220822-1", "1-alpha-20230711-2"]:
            self.targets[ver] = f"https://github.com/linuxdeploy/linuxdeploy/releases/download/{ver}/linuxdeploy-x86_64.AppImage"
            # add version to file name to allow downloading multiple versions
            self.archiveNames[ver] = f"linuxdeploy-{ver}-x86_64.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.targetDigests["1-alpha-20220822-1"] = (["fb9183b0cac3985829f8dbcdcaa2bc0fa4bb7db0e1a7215e23f52f31088c993d"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1-alpha-20230711-2"] = (["d9e7ba27f0d9a45d5ebdcb8fb363339f0cf1cfed918586a2982e4b46c342cc08"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1-alpha-20230711-2"
        self.description = "AppDir creation and maintenance tool. Featuring flexible plugin system."
        self.webpage = "https://github.com/linuxdeploy/linuxdeploy"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/linuxdeploy-plugin-qt"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not super().install():
            return False
        # remove version from file name
        return utils.moveFile(self.installDir() / self.subinfo.archiveNames[self.buildTarget], self.installDir() / "linuxdeploy-x86_64.AppImage")
