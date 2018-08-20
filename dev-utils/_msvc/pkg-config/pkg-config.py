import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        build = "56"
        for ver in ["0.29.2"]:
            self.targets[ ver ] = f"https://files.kde.org/craft/autotools/packages/pkg-config-{ver}-{build}-windows-mingw_{CraftCore.compiler.bits}-gcc.7z"
            self.targetDigestUrls[ ver ] = f"https://files.kde.org/craft/autotools/packages/pkg-config-{ver}-{build}-windows-mingw_{CraftCore.compiler.bits}-gcc.7z.sha256"
            self.targetInstallPath[ ver ] = "dev-utils/pkg-config"
        self.defaultTarget = "0.29.2"

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = "default"

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not super().install():
            return False
        return utils.createShim(os.path.join(self.imageDir(), "bin", "pkg-config.exe"), os.path.join(self.installDir(), "bin", "pkg-config.exe"))
