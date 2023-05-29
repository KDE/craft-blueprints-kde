import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(
            tarballUrl="http://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/kirigami2-${VERSION}.tar.xz",
            tarballDigestUrl="http://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/kirigami2-${VERSION}.tar.xz.sha1",
            tarballInstallSrc="kirigami2-${VERSION}",
        )

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


from Blueprints.CraftPackageObject import CraftPackageObject


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        CraftPackageObject.get("kde").pattern.__init__(self)
