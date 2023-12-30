import info
import utils
from CraftStandardDirs import CraftStandardDirs
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "headers required to interface with Nvidias codec APIs"
        for ver in ["11.1.5.0", "12.0.16.0", "12.1.14.0"]:
            self.targets[ver] = f"https://github.com/FFmpeg/nv-codec-headers/archive/refs/tags/n{ver}.tar.gz"
            self.targetInstSrc[ver] = "nv-codec-headers-n" + ver
            self.patchToApply[ver] = ("", 0)
        self.targetDigests["11.1.5.0"] = (["b833bd90852c1f45d01f65c70545f6a31e5b9ca64814a269626c7ad2286d55ee"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["12.0.16.0"] = (["2a1533b65f55f9da52956faf0627ed3b74868ac0c7f269990edd21369113b48f"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["12.1.14.0"] = (["2fefaa227d2a3b4170797796425a59d1dd2ed5fd231db9b4244468ba327acd0b"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "12.1.14.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def install(self):
        with open(self.sourceDir() / "ffnvcodec.pc.in", "rt") as f:
            content = f.read()
        content = content.replace("@@PREFIX@@", str(CraftStandardDirs.craftRoot()))
        utils.createDir(self.installDir() / "lib/pkgconfig/")
        with open(self.installDir() / "lib/pkgconfig/ffnvcodec.pc", "wt") as f:
            f.write(content)
        return utils.copyDir(self.sourceDir() / "include", self.installDir() / "include")
