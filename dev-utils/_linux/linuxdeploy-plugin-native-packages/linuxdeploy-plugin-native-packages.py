import stat
from pathlib import Path

import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets[
            "continous"
        ] = "https://github.com/linuxdeploy/linuxdeploy-plugin-native_packages/releases/download/continuous/linuxdeploy-plugin-native_packages-x86_64.AppImage"
        self.targetInstallPath["continous"] = "dev-utils/bin"
        self.description = "Experimental linuxdeploy plugin that creates native packages (`.rpm`, `.deb`) from AppDirs."
        self.webpage = "https://github.com/linuxdeploy/linuxdeploy-plugin-native_packages"
        self.defaultTarget = "continous"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/rpm"] = None
        self.buildDependencies["dev-utils/dpkg"] = None


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
