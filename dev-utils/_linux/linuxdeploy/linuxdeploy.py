import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1-alpha-20250213-2", "1-alpha-20251107-1"]:
            self.targets[ver] = (
                f"https://github.com/linuxdeploy/linuxdeploy/releases/download/{ver}/linuxdeploy-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
            )
            # add version to file name to allow downloading multiple versions
            self.archiveNames[ver] = f"linuxdeploy-{ver}-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"

        for ver in ["continuous-20261001"]:
            self.targets[ver] = (
                f"https://files.kde.org/craft/sources/dev-utils/linuxdeploy/{ver}/linuxdeploy-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
            )
            # add version to file name to allow downloading multiple versions
            self.archiveNames[ver] = f"linuxdeploy-{ver}-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"

        self.targets["continous"] = (
            f"https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
        )
        self.targetInstallPath["continous"] = "dev-utils/bin"

        if CraftCore.compiler.architecture.isArm64:
            self.targetDigests["1-alpha-20250213-2"] = (["06706ac8189797dccd36bd384105892cb5e6e71f784f4df526cc958adc223cd6"], CraftHash.HashAlgorithm.SHA256)
            self.targetDigests["1-alpha-20251107-1"] = (["620095110d693282b8ebeb244a95b5e911cf8f65f76c88b4b47d16ae6346fcff"], CraftHash.HashAlgorithm.SHA256)
            self.targetDigests["continuous-20261001"] = (["5c1fddf96066891e829831cac0d84424690f3b22846c7f8f1bb9990a5c6c73f4"], CraftHash.HashAlgorithm.SHA256)
        else:
            self.targetDigests["1-alpha-20250213-2"] = (["4648f278ab3ef31f819e67c30d50f462640e5365a77637d7e6f2ad9fd0b4522a"], CraftHash.HashAlgorithm.SHA256)
            self.targetDigests["1-alpha-20251107-1"] = (["c20cd71e3a4e3b80c3483cef793cda3f4e990aca14014d23c544ca3ce1270b4d"], CraftHash.HashAlgorithm.SHA256)
            self.targetDigests["continuous-20261001"] = (["8aea8da0f7f7039d2a2cecb14657d752a222a5e1d3825caeef186c82f751cdd1"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "continuous-20261001"

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
        dest = self.installDir() / f"linuxdeploy-{CraftCore.compiler.architecture.appImageArchitecture}.AppImage"
        if self.subinfo.buildTarget != "continous":
            # remove version from file name
            return utils.moveFile(self.installDir() / self.subinfo.archiveNames[self.buildTarget], dest)
        else:
            # hack enforce redownload on update
            utils.deleteFile(self.localFilePath()[0])
            return utils.moveFile(self.installDir() / self.localFileNames()[0], dest)
