import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/uclouvain/openjpeg.git"

        self.patchToApply["2.5.0"] = [
            ("338246278a8e753c36e8319044360eb7a84f6488.diff", 1),
        ]

        for ver in ["2.1.2", "2.3.0", "2.4.0", "2.5.0", "2.5.3"]:
            self.targets[ver] = f"https://github.com/uclouvain/openjpeg/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"openjpeg-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"openjpeg-{ver}"
        self.targetDigests["2.1.2"] = (["4ce77b6ef538ef090d9bde1d5eeff8b3069ab56c4906f083475517c2c023dfa7"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.3.0"] = (["3dc787c1bb6023ba846c2a0d9b1f6e179f1cd255172bde9eb75b01f1e6c7d71a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.4.0"] = (["8702ba68b442657f11aaeb2b338443ca8d5fb95b0d845757968a7be31ef7f16d"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.0"] = (["0333806d6adecc6f7a91243b2b839ff4d2053823634d4f6ed7a59bc87409122a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.3"] = (["368fe0468228e767433c9ebdea82ad9d801a3ad1e4234421f352c8b06e7aa707"], CraftHash.HashAlgorithm.SHA256)

        self.description = "OpenJPEG is an open-source JPEG 2000 codec written in C language."
        self.webpage = "http://www.openjpeg.org/"
        self.defaultTarget = "2.5.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/lcms2"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
