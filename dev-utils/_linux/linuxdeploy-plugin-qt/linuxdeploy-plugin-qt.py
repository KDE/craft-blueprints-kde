import stat
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.0.0-alpha-1-20250119"]:
            self.targets[
                ver
            ] = f"https://github.com/linuxdeploy/linuxdeploy-plugin-qt/releases/download/{ver}/linuxdeploy-plugin-qt-static-{CraftCore.compiler.appImageArchitecture}.AppImage"
            # add version to file name to allow downloading multiple versions
            self.archiveNames[ver] = f"linuxdeploy-plugin-qt-{ver}-{CraftCore.compiler.appImageArchitecture}.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.targets[
            "continous"
        ] = f"https://github.com/linuxdeploy/linuxdeploy-plugin-qt/releases/download/continuous/linuxdeploy-plugin-qt-static-{CraftCore.compiler.appImageArchitecture}.AppImage"
        self.targetInstallPath["continous"] = "dev-utils/bin"
        self.description = "AppDir creation and maintenance tool. Featuring flexible plugin system."
        self.webpage = "https://github.com/linuxdeploy/linuxdeploy"
        self.targetDigests["2.0.0-alpha-1-20250119"] = (['902eb77cb9d2c8f77403c0bae89b992bb1e2f7128b118a666c65ebc7d76173ff'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.0.0-alpha-1-20250119"

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
