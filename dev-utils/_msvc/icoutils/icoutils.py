import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild("dev-utils/_autotools/icoutils", targetInstallPath=os.path.join("dev-utils", "bin"))

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)


    def install(self):
        if not super().install():
            return False
        return (utils.createShim(os.path.join(self.imageDir(), "bin", "icotool.exe"), os.path.join(self.installDir(), "bin", "icotool.exe")) and
                utils.createShim(os.path.join(self.imageDir(), "bin", "wrestool.exe"), os.path.join(self.installDir(), "bin", "wrestool.exe")) )
