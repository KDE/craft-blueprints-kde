import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1-alpha-20250213-2"]:
            self.targets[
                ver
            ] = f"https://github.com/linuxdeploy/linuxdeploy/releases/download/{ver}/linuxdeploy-{CraftCore.compiler.appImageArchitecture}.AppImage"
            # add version to file name to allow downloading multiple versions
            self.archiveNames[ver] = f"linuxdeploy-{ver}-{CraftCore.compiler.appImageArchitecture}.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.targets[
            "continous"
        ] = f"https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-{CraftCore.compiler.appImageArchitecture}.AppImage"
        self.targetInstallPath["continous-static"] = "dev-utils/bin"
        self.targetDigests["1-alpha-20250213-2"] = (["4648f278ab3ef31f819e67c30d50f462640e5365a77637d7e6f2ad9fd0b4522a"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1-alpha-20250213-2"

        self.description = "AppDir creation and maintenance tool. Featuring flexible plugin system."
        self.webpage = "https://github.com/linuxdeploy/linuxdeploy"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/linuxdeploy-plugin-qt"] = None
        self.runtimeDependencies["dev-utils/linuxdeploy-plugin-appimage"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False
        if self.subinfo.buildTarget != "continous-static":
            # remove version from file name
            return utils.moveFile(self.installDir() / self.subinfo.archiveNames[self.buildTarget], self.installDir() / "linuxdeploy-x86_64.AppImage")
        else:
            # hack enforce redownload on update
            utils.deleteFile(self.localFilePath()[0])
            return utils.moveFile(self.installDir() / self.localFileNames()[0], self.installDir() / "linuxdeploy-x86_64.AppImage")
