import os

import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "2.5.14"
        self.targets[ver] = f"https://downloads.sourceforge.net/sourceforge/winflexbison/win_flex_bison-{ver}.zip"
        self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")
        self.targetDigests[ver] = "e15a1b8780a36ffda9ef70c4f09283867b32a12b"
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
