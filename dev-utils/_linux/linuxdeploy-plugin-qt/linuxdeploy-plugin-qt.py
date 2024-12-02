import stat
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1-alpha-20240109-1", "2.0.0-alpha-1-20241106"]:
            self.targets[
                ver
            ] = f"https://github.com/linuxdeploy/linuxdeploy-plugin-qt/releases/download/{ver}/linuxdeploy-plugin-qt-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
            # add version to file name to allow downloading multiple versions
            self.archiveNames[ver] = f"linuxdeploy-plugin-qt-{ver}-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.targets[
            "continous"
        ] = f"https://github.com/linuxdeploy/linuxdeploy-plugin-qt/releases/download/continuous/linuxdeploy-plugin-qt-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
        self.targetInstallPath["continous"] = "dev-utils/bin"
        self.description = "AppDir creation and maintenance tool. Featuring flexible plugin system."
        self.webpage = "https://github.com/linuxdeploy/linuxdeploy"
        self.targetDigests["2.0.0-alpha-1-20241106"] = (["0615e9218606f14d38be37ef88908dee1ce6c32a04ad0e4f18dff9a85fa2e217"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1-alpha-20240109-1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
