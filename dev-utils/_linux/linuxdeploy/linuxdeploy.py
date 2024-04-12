import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1-alpha-20240109-1"]:
            self.targets[
                ver
            ] = f"https://github.com/linuxdeploy/linuxdeploy/releases/download/{ver}/linuxdeploy-static-{CraftCore.compiler.appImageArchitecture}.AppImage"
            # add version to file name to allow downloading multiple versions
            self.archiveNames[ver] = f"linuxdeploy-{ver}-{CraftCore.compiler.appImageArchitecture}.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.targets[
            "continous-static"
        ] = f"https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-static-{CraftCore.compiler.appImageArchitecture}.AppImage"
        self.targetInstallPath["continous-static"] = "dev-utils/bin"
        self.targetDigests["1-alpha-20231206-1"] = (["80de10fa339564d78e50cbde8dd27d012b7c2274291006506d22b4eb494bc7a3"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1-alpha-20240109-1"

        self.description = "AppDir creation and maintenance tool. Featuring flexible plugin system."
        self.webpage = "https://github.com/linuxdeploy/linuxdeploy"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/linuxdeploy-plugin-qt"] = None
        self.runtimeDependencies["dev-utils/linuxdeploy-plugin-appimage"] = None


from Package.BinaryPackageBase import *


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
