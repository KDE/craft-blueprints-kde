import os

import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "2.5.25"
        self.targets[ver] = f"https://github.com/lexxmark/winflexbison/releases/download/v{ver}/win_flex_bison-{ver}.zip"
        self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")
        self.targetDigests[ver] = (["8d324b62be33604b2c45ad1dd34ab93d722534448f55a16ca7292de32b6ac135"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies["dev-utils/wget"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False

    def install(self):
        if not super().install():
            return False
        return utils.copyFile(self.installDir() / "win_flex.exe", self.installDir() / "flex.exe") and utils.copyFile(
            self.installDir() / "win_bison.exe", self.installDir() / "bison.exe"
        )
