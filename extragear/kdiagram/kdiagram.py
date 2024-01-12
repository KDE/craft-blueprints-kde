import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Powerful libraries (KChart, KGantt) for creating business diagrams"

        for ver in ["2.8.0", "3.0.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/kdiagram/{ver}/kdiagram-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/kdiagram/{ver}/kdiagram-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"kdiagram-{ver}"

        self.svnTargets["master"] = "https://invent.kde.org/graphics/kdiagram.git"
        self.targetUpdatedRepoUrl["master"] = ("https://anongit.kde.org/kdiagram", "https://invent.kde.org/graphics/kdiagram.git")

        self.defaultTarget = "2.8.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/qt/qtsvg"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
