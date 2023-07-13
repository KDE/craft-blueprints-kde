import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1-alpha-20230711-2", "1-alpha-20230712-1"]:
            self.targets[ver] = f"https://github.com/linuxdeploy/linuxdeploy/releases/download/{ver}/linuxdeploy-x86_64.AppImage"
            # add version to file name to allow downloading multiple versions
            self.archiveNames[ver] = f"linuxdeploy-{ver}-x86_64.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.targets["continous-static"] = "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-static-x86_64.AppImage"
        self.targetDigests["1-alpha-20230711-2"] = (["d9e7ba27f0d9a45d5ebdcb8fb363339f0cf1cfed918586a2982e4b46c342cc08"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1-alpha-20230712-1"] = (["9a86c10bce48e4570d95897092b758d306500dc58c26ce0564706caea3cbb192"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "continous-static"
        self.description = "AppDir creation and maintenance tool. Featuring flexible plugin system."
        self.webpage = "https://github.com/linuxdeploy/linuxdeploy"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/linuxdeploy-plugin-qt"] = None
        self.runtimeDependencies["dev-utils/linuxdeploy-plugin-appimage"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)

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
