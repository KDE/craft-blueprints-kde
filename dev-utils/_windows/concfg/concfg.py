import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/lukesampson/concfg.git"
        self.targetInstallPath["master"] = "dev-utils/concfg/"

        self.description = "Concfg is a utility to import and export Windows console settings like fonts and colors."
        self.webpage = "https://github.com/lukesampson/concfg"

        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        super().__init__()

    def unpack(self):
        return True

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        utils.createShim(
            os.path.join(self.imageDir(), "dev-utils", "bin", "concfg.exe"),
            CraftCore.cache.findApplication("powershell"),
            args="-NoProfile {path}".format(path=os.path.join(self.imageDir(), "dev-utils", "concfg", "bin", "concfg.ps1")),
            useAbsolutePath=True,
        )
        return True
