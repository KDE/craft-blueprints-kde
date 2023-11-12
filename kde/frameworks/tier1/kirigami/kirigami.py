import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            self.versionInfo.setDefaultValues(
                tarballUrl="https://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/kirigami2-${VERSION}.tar.xz",
                tarballDigestUrl="https://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/kirigami2-${VERSION}.tar.xz.sha1",
                tarballInstallSrc="kirigami2-${VERSION}",
            )
        else:
            self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            self.runtimeDependencies["libs/qt5/qtgraphicaleffects"] = None
            self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        else:
            self.runtimeDependencies["libs/qt/qtsvg"] = None
            self.runtimeDependencies["libs/qt/qttools"] = None
            self.runtimeDependencies["libs/qt6/qt5compat"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
