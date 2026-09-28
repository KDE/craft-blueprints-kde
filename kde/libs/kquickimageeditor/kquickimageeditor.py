import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/kquickimageeditor.git"

        for ver in ["0.5.1", "0.7.0.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/kquickimageeditor/kquickimageeditor-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kquickimageeditor-{ver}"

        self.description = "A set of QtQuick components providing basic image editing capabilities"
        self.targetDigests["0.5.1"] = (["f08271f368ead077fa3ed95c32446dd873f8b371d9756aefb757bea323339b29"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.7.0.1"] = (["b65f32c44bd126cea5e1b5a6eb7cb0eb517277cb8de06675fa6be624b7da381a"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.7.0.1"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/libhwy"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
