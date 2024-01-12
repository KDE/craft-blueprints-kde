import info
from CraftCompiler import CraftCompiler


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedBuild(
            "https://files.kde.org/craft/prebuilt/packages/22.11",
            packageName="dev-utils/_autotools/icoutils",
            targetInstallPath="dev-utils",
            architecture=CraftCompiler.Architecture.x86_64,
        )
        self.patchLevel["0.32.3"] = 1

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **args):
        super().__init__()

    def install(self):
        if not super().install():
            return False
        return utils.createShim(
            os.path.join(self.imageDir(), "dev-utils", "bin", "icotool.exe"), os.path.join(self.installDir(), "bin", "icotool.exe")
        ) and utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "wrestool.exe"), os.path.join(self.installDir(), "bin", "wrestool.exe"))
