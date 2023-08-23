import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedBuild("https://files.kde.org/craft/prebuilt/packages/22.11", packageName="dev-utils/_autotools/grep", targetInstallPath="dev-utils")

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def postInstall(self):
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "grep.exe"), os.path.join(self.installDir(), "bin", "grep.exe"))
