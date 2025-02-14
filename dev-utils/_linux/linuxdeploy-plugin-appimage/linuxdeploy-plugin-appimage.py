import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1-alpha-20250213-1"]:
            self.targets[
                ver
            ] = f"https://github.com/linuxdeploy/linuxdeploy-plugin-appimage/releases/download/{ver}/linuxdeploy-plugin-appimage-{CraftCore.compiler.appImageArchitecture}.AppImage"
            # add version to file name to allow downloading multiple versions
            self.archiveNames[ver] = f"linuxdeploy-plugin-appimage-{ver}-{CraftCore.compiler.appImageArchitecture}.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.targetDigests["1-alpha-20250213-1"] = (["992d502a248e14ab185448ddf6f6e7d25558cb84d4623c354c3af350c25fccb3"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1-alpha-20250213-1"
        self.description = "Plugin for linuxdeploy. Creates AppImages from AppDirs."
        self.webpage = "https://github.com/linuxdeploy/linuxdeploy-plugin-appimage"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False
        # remove version from file name
        return utils.moveFile(
            self.installDir() / self.subinfo.archiveNames[self.buildTarget], self.installDir() / "linuxdeploy-plugin-appimage-x86_64.AppImage"
        )
