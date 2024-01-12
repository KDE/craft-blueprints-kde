import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "SnoreToast"
        self.description = "A command line application capable of creating Windows Toast notifications."
        self.webpage = "https://invent.kde.org/libraries/snoretoast"

        self.svnTargets["master"] = "https://invent.kde.org/libraries/snoretoast.git"
        self.targetUpdatedRepoUrl["master"] = ("https://anongit.kde.org/snoretoast", "https://invent.kde.org/libraries/snoretoast.git")

        for ver in ["0.5.2", "0.6.0", "0.7.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/snoretoast/{ver}/src/snoretoast-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/snoretoast/{ver}/src/snoretoast-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"snoretoast-{ver}"

        for ver in ["0.8.0", "0.9.0"]:
            self.targets[ver] = f"https://invent.kde.org/libraries/snoretoast/-/archive/v{ver}/snoretoast-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"snoretoast-v{ver}"
        self.targetDigests["0.8.0"] = (["3d77ae76dd47929c088b3bbf4bd4fa2984dfa3c8c4c959ad4a5a427002a2ab64"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.9.0"] = (["2d19d793b665ec0357a506111528110f87823c3efcd1a08599e1c4571ae86066"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.9.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()

    def qmerge(self):
        OsUtils.killProcess("snoretoast", CraftCore.standardDirs.craftRoot())
        return super().qmerge()
