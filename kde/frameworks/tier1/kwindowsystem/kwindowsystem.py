import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KWindowSystem"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.runtimeDependencies["libs/wayland-protocols"] = None
            self.runtimeDependencies["libs/qt/qtwayland"] = None
            self.runtimeDependencies["kde/libs/plasma-wayland-protocols"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            if OsUtils.isUnix():
                self.runtimeDependencies["libs/qt5/qtx11extras"] = None
            else:
                self.runtimeDependencies["libs/qt5/qtwinextras"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
