import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "SnoreToast"
        self.description = "A command line application capable of creating Windows Toast notifications."
        self.webpage = "https://invent.kde.org/libraries/snoretoast"

        self.svnTargets["master"] = "https://invent.kde.org/libraries/snoretoast.git"
        self.targetUpdatedRepoUrl["master"] = ("https://anongit.kde.org/snoretoast", "https://invent.kde.org/libraries/snoretoast.git")
        self.defaultTarget = "0.7.0"

        for ver in ["0.5.2", "0.6.0", "0.7.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/snoretoast/{ver}/src/snoretoast-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/snoretoast/{ver}/src/snoretoast-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"snoretoast-{ver}"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
