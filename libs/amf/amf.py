import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "AMD library for accelerated H.264 and HEVC(only windows) encoding on hardware with Video Coding Engine (VCE)"
        for ver in ["1.4.36", "1.5.2"]:
            self.targets[ver] = f"https://github.com/GPUOpen-LibrariesAndSDKs/AMF/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "AMF-" + ver
        self.targetDigests["1.4.36"] = (["240a42033babc7920e5476506d5ac0c5628f67908833168e746406808d0ef146"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.5.2"] = (["d3c12eb324edf05e214608b6a395a51dd95770ed9d45520185d6c3a206811c99"], CraftHash.HashAlgorithm.SHA256)
        self.webpage = "https://github.com/GPUOpen-LibrariesAndSDKs/AMF"
        self.defaultTarget = "1.5.2"


class Package(BinaryPackageBase):
    def install(self):
        return utils.createDir(self.installDir() / "include/AMF") and utils.copyDir(self.sourceDir() / "amf/public/include", self.installDir() / "include/AMF")
