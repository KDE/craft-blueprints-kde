import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild("dev-utils/_autotools/pkg-config", targetInstallPath=os.path.join("dev-utils", "bin"))

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = None

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not super().install():
            return False
        return utils.createShim(os.path.join(self.imageDir(), "bin", "pkg-config.exe"), os.path.join(self.installDir(), "bin", "pkg-config.exe"))
