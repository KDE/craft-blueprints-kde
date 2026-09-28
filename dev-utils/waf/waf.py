import stat
from pathlib import Path

import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.1.9"]:
            self.targets[ver] = f"https://waf.io/waf-{ver}"
            self.archiveNames[ver] = f"waf-{ver}"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.targetDigests["2.1.9"] = (["e235eeac6d34f039834e355a738298416a92a17defd1b6e1eae48488ba4a6864"], CraftHash.HashAlgorithm.SHA256)
        self.description = "A Python-based build system"
        self.webpage = "https://waf.io/"
        self.defaultTarget = "2.1.9"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def unpack(self):
        return True

    def install(self):
        if not self.cleanImage():
            return False

        utils.createDir(self.installDir())
        src = Path(self.localFilePath()[0])
        dest = self.installDir() / "waf"
        if not utils.copyFile(src, dest, linkOnly=False):
            return False
        dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return True
