import info
import utils
from Package.SourceOnlyPackageBase import SourceOnlyPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "AMD library for accelerated H.264 and HEVC(only windows) encoding on hardware with Video Coding Engine (VCE)"
        for ver in ["1.4.35"]:
            self.targets[ver] = f"https://github.com/GPUOpen-LibrariesAndSDKs/AMF/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "AMF-" + ver
        self.targetDigests["1.4.35"] = (["5d93101eae5895247bea58cff40bb84424158170ae7f931105666157cc187636"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.4.35"


class Package(SourceOnlyPackageBase):
    def install(self):
        utils.createDir(self.installDir() / "include/AMF")
        return utils.copyDir(self.sourceDir() / "amf/public/include", self.installDir() / "include/AMF")
