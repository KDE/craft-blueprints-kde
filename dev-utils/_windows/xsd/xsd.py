import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for version in ["4.0.0"]:
            self.targets[version] = f"http://codesynthesis.com/download/xsd/{version[:3]}/windows/i686/xsd-{version}-i686-windows.zip"
            self.targetInstSrc[version] = f"xsd-{version}-i686-windows"
            self.targetInstallPath[version] = "dev-utils/xsd"
        self.targetDigests["4.0.0"] = (["73c478ea76c9847bdd292f4db80900b93a9798334687999e54e5796971f11dc1"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "4.0.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False
        return utils.createShim(self.imageDir() / "dev-utils/bin/xsd.exe", self.imageDir() / "dev-utils/xsd/bin/xsd.exe")
