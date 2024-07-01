import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/uclouvain/openjpeg.git"

        self.patchToApply["2.5.0"] = [
            ("338246278a8e753c36e8319044360eb7a84f6488.diff", 1),
        ]

        for ver in ["2.1.2", "2.3.0", "2.4.0", "2.5.0", "2.5.2"]:
            self.targets[ver] = f"https://github.com/uclouvain/openjpeg/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"openjpeg-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"openjpeg-{ver}"
        self.targetDigests["2.1.2"] = (["4ce77b6ef538ef090d9bde1d5eeff8b3069ab56c4906f083475517c2c023dfa7"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.3.0"] = (["3dc787c1bb6023ba846c2a0d9b1f6e179f1cd255172bde9eb75b01f1e6c7d71a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.4.0"] = (["8702ba68b442657f11aaeb2b338443ca8d5fb95b0d845757968a7be31ef7f16d"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.0"] = (["0333806d6adecc6f7a91243b2b839ff4d2053823634d4f6ed7a59bc87409122a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.2"] = (["90e3896fed910c376aaf79cdd98bdfdaf98c6472efd8e1debf0a854938cbda6a"], CraftHash.HashAlgorithm.SHA256)

        self.description = "OpenJPEG is an open-source JPEG 2000 codec written in C language."
        self.webpage = "http://www.openjpeg.org/"
        self.defaultTarget = "2.5.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/lcms2"] = None
        self.runtimeDependencies["libs/zlib"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
