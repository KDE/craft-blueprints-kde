import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["2.2"] = "https://invent.kde.org/kdevelop/kdevelop-pg-qt.git|2.2"
        self.svnTargets["master"] = "https://invent.kde.org/kdevelop/kdevelop-pg-qt.git"
        self.defaultTarget = "2.2"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
