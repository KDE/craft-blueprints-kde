import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver, fullVer in [("5.2", "9232_v5.2-4-ge724fdcb")]:
            self.targets[ver] = f"https://files.lhmouse.com/nano-win/nano-win_{fullVer}.7z"
            self.targetInstallPath[ver] = "dev-utils/nano/"

        self.targetDigests["5.2"] = (["4606143ceb2c730e440664f8dba4fa7d1e7f435d29783b39dc88bee9d265134d"], CraftHash.HashAlgorithm.SHA256)
        self.webpage = "https://github.com/lhmouse/nano-win"
        self.description = "GNU nano text editor for Windows"
        self.defaultTarget = "5.2"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        super().__init__()

    def unpack(self):
        if not super().unpack():
            return False
        return utils.rmtree(self.sourceDir() / "i686-w64-mingw32") and utils.mergeTree(self.sourceDir() / "x86_64-w64-mingw32", self.sourceDir())

    def install(self):
        if not super().install():
            return False
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "nano.exe"), os.path.join(self.installDir(), "bin", "nano.exe"))
