import stat
from pathlib import Path

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["continous"] = ["https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"]
        self.targetInstallPath["continous"] = "dev-utils/bin"
        self.description = "Converts an AppDir into a self-mounting filesystem image"
        self.webpage = "https://github.com/AppImage/AppImageKit"
        self.defaultTarget = "continous"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **args):
        super().__init__()

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
