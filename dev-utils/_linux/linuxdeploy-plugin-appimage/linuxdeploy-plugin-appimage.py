import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1-alpha-20250213-1"]:
            self.targets[ver] = (
                f"https://github.com/linuxdeploy/linuxdeploy-plugin-appimage/releases/download/{ver}/linuxdeploy-plugin-appimage-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
            )
            # add version to file name to allow downloading multiple versions
            self.archiveNames[ver] = f"linuxdeploy-plugin-appimage-{ver}-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"
        if CraftCore.compiler.architecture.isArm64:
            self.targetDigests["1-alpha-20250213-1"] = (["83c292149274965a865dcd44c135cfca8ba28c6b7de3eb628d4b8b5f248af17c"], CraftHash.HashAlgorithm.SHA256)
        else:
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
            self.installDir() / self.subinfo.archiveNames[self.buildTarget],
            self.installDir() / f"linuxdeploy-plugin-appimage-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage",
        )
