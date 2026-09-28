import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "MpvQt"
        self.description = "MpvQt is a libmpv wrapper for QtQuick2 and QML"
        self.svnTargets["master"] = "https://invent.kde.org/libraries/mpvqt"
        self.defaultTarget = "1.2.0"

        for ver in ["1.2.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/mpvqt/mpvqt-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"mpvqt-{ver}"
            self.archiveNames[ver] = f"mpvqt-{ver}.tar.gz"

        self.targetDigests["1.2.0"] = (["8660ad79c0d60fed77f29b36e1742841466af5405de702c81a121e6eeb625ebb"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/mpv"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
