import stat
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.9.1", "continuous"]:
            self.targets[ver] = [
                f"https://github.com/AppImage/appimagetool/releases/download/{ver}/appimagetool-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
            ]
            self.targetInstallPath[ver] = "dev-utils/bin"
        if CraftCore.compiler.architecture.isArm64:
            self.targetDigests["1.9.1"] = (["f0837e7448a0c1e4e650a93bb3e85802546e60654ef287576f46c71c126a9158"], CraftHash.HashAlgorithm.SHA256)
        else:
            self.targetDigests["1.9.1"] = (["ed4ce84f0d9caff66f50bcca6ff6f35aae54ce8135408b3fa33abfc3cb384eb0"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Converts an AppDir into a self-mounting filesystem image"
        self.webpage = "https://github.com/AppImage/appimagetool"
        self.defaultTarget = "1.9.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def unpack(self):
        return True

    def install(self):
        utils.createDir(self.installDir())
        for f in self.localFilePath():
            src = Path(f)
            dest = Path(self.installDir()) / src.name
            # we move the files so that on a reinstall the continuous target gets redownloaded
            if not utils.moveFile(src, dest):
                return False
            dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return True
