import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.3.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/kdevelop-pg-qt/{ver}/src/kdevelop-pg-qt-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/kdevelop-pg-qt/{ver}/src/kdevelop-pg-qt-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"kdevelop-pg-qt-{ver}"

        self.svnTargets["master"] = "https://invent.kde.org/kdevelop/kdevelop-pg-qt.git"
        self.defaultTarget = "2.3.0"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
