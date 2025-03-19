import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "the poppler CJK encoding data"
        self.svnTargets["master"] = "https://invent.kde.org/mirrors/poppler-data.git"

        # use poppler data matching the latest poppler release used in poppler.py
        for ver in ["0.4.11", "0.4.12"]:
            dashVer = ver.replace(".", "_")
            self.targets[ver] = f"https://invent.kde.org/mirrors/poppler-data/-/archive/POPPLER_DATA_{dashVer}/poppler-data-POPPLER_DATA_{dashVer}.tar.bz2"
            self.targetInstSrc[ver] = f"poppler-data-POPPLER_DATA_{dashVer}"
        self.targetDigests["0.4.12"] = (["058c83f06e7ad56d46b8e7fa8a7ff4e8a62a69c8738dc25acde95fa4270d9bc4"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.4.12"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
