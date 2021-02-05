import info


class subinfo(info.infoclass):
    def setTargets(self):
        platform = CraftCore.compiler.platform.name.lower()
        ext = "tar.gz"
        if CraftCore.compiler.isMacOS:
            platform = "Darwin"
        if CraftCore.compiler.isWindows:
            platform = "Windows"
            ext = "zip"
        for ver in ["0.4.0", "0.5.0", "0.6.0"]:
            self.targets[ver] = f"https://github.com/muesli/duf/releases/download/v{ver}/duf_{ver}_{platform}_x86_64.{ext}"
            self.targetInstallPath[ver] = "dev-utils/duf"
            self.targetDigestUrls[ver] = (f"https://github.com/muesli/duf/releases/download/v{ver}/checksums.txt", CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.6.0"

        self.description = "Disk Usage/Free Utility"
        self.webpage = "https://github.com/muesli/duf"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def postInstall(self):
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", f"duf{CraftCore.compiler.executableSuffix}"),
                                os.path.join(self.imageDir(), "dev-utils", "duf", f"duf{CraftCore.compiler.executableSuffix}"))