import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/mpvqt"
        self.displayName = "MpvQt"
        self.description = "MpvQt is a libmpv wrapper for QtQuick2 and QML"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/mpv"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()
