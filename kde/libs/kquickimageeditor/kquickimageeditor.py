import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/kquickimageeditor.git"

        for ver in ["0.3.0"]:
            self.targets[ver] = "https://download.kde.org/stable/kquickimageeditor/kquickimageeditor-%s.tar.xz" % ver
            self.archiveNames[ver] = "kquickimageeditor-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "kquickimageeditor-%s" % ver

        self.description = "A set of QtQuick components providing basic image editing capabilities"
        self.defaultTarget = "0.3.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()
