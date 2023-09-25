import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/graphics/kdiagram.git"
        self.targetUpdatedRepoUrl["master"] = ("https://anongit.kde.org/kdiagram", "https://invent.kde.org/graphics/kdiagram.git")
        self.defaultTarget = "master"

        self.description = "Powerful libraries (KChart, KGantt) for creating business diagrams"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/qt/qtsvg"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
