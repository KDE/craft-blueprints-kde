import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        for ver in ["3.03", "3.09"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/sourceforge/nsis/nsis-{ver}.zip"
            self.targetInstSrc[ver] = f"nsis-{ver}"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "nsis")

        self.targetDigests["3.03"] = (["b53a79078f2c6abf21f11d9fe68807f35b228393eb17a0cd3873614190116ba7"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.09"] = (["f5dc52eef1f3884230520199bac6f36b82d643d86b003ce51bd24b05c6ba7c91"], CraftHash.HashAlgorithm.SHA256)

        self.webpage = "http://nsis.sourceforge.net"
        self.defaultTarget = "3.09"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        super().__init__()

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        CraftCore.cache.clear()
        for name in ["makensis", "makensisw", "nsis"]:
            if not utils.createShim(
                os.path.join(self.imageDir(), "dev-utils", "bin", f"{name}.exe"), os.path.join(self.imageDir(), "dev-utils", "nsis", f"{name}.exe")
            ):
                return False
        return True

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
