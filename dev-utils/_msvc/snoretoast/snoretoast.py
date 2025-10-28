import info
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "SnoreToast"
        self.description = "A command line application capable of creating Windows Toast notifications."
        self.webpage = "https://invent.kde.org/libraries/snoretoast"

        self.svnTargets["master"] = "https://invent.kde.org/libraries/snoretoast.git"
        self.targetUpdatedRepoUrl["master"] = ("https://anongit.kde.org/snoretoast", "https://invent.kde.org/libraries/snoretoast.git")

        for ver in ["0.9.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/snoretoast/snoretoast-v{ver}.tar.bz2"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/snoretoast/snoretoast-v{ver}.tar.bz2.sha256"
            self.targetInstSrc[ver] = f"snoretoast-v{ver}"
        self.defaultTarget = "0.9.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def qmerge(self):
        OsUtils.killProcess("snoretoast", CraftCore.standardDirs.craftRoot())
        return super().qmerge()
