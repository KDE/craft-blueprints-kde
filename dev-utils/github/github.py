import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.tags = "hub"
        platform = CraftCore.compiler.platform.name.lower()
        ext = "tgz"
        if CraftCore.compiler.isMacOS:
            platform = "darwin"
        if CraftCore.compiler.isWindows:
            ext = "zip"
        for ver in ["2.14.2"]:
            self.targets[ver] = f"https://github.com/github/hub/releases/download/v{ver}/hub-{platform}-amd64-{ver}.{ext}"
            if not CraftCore.compiler.isWindows:
                self.targetInstSrc[ver] = f"hub-{platform}-amd64-{ver}"
            self.targetInstallPath[ver] = "dev-utils/github"
        self.defaultTarget = "2.14.2"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def postInstall(self):
        return utils.createShim(
            os.path.join(self.imageDir(), "dev-utils", "bin", f"hub{CraftCore.compiler.executableSuffix}"),
            os.path.join(self.imageDir(), "dev-utils", "github", "bin", f"hub{CraftCore.compiler.executableSuffix}"),
        )
