import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/graphics/kdiagram.git"
        self.targetUpdatedRepoUrl["master"] = ("git://anongit.kde.org/kdiagram", "https://invent.kde.org/graphics/kdiagram.git")
        self.defaultTarget = "master"
        # otherwise undefined KGantt::Constraint while building tests
        if CraftCore.compiler.isMacOS:
            self.patchToApply["master"] = [("kdiagram-20181019.patch", 1)]

        self.description = "Powerful libraries (KChart, KGantt) for creating business diagrams"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/qt5/qtsvg"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
