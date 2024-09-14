import info
import utils
from CraftCompiler import CraftCompiler
from Package.BinaryPackageBase import BinaryPackageBase


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


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False
        return utils.createShim(self.imageDir() / "dev-utils/bin/icotool.exe", self.installDir() / "bin/icotool.exe") and utils.createShim(
            self.imageDir() / "dev-utils/bin/wrestool.exe", self.installDir() / "bin/wrestool.exe"
        )
