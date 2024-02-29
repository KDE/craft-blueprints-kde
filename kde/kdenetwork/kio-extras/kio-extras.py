import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Extra plugins for KIO (thumbnail generators, archives, remote filesystems and more)"

        # kio-extras is a special case, it releases different tarballs for Qt5 and Qt6
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            ver = self.subinfo.defaultTarget
            self.targets[ver] = f"https://download.kde.org/stable/release-service/{ver}/src/kio-extras-kf5-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/release-service/{ver}/src/kio-extras-kf5-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"kio-extras-kf5-{ver}"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/libssh"] = None
        self.runtimeDependencies["libs/openexr"] = None
        self.runtimeDependencies["libs/taglib"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        # self.runtimeDependencies["qt-libs/kdsoap"] = None # Our KDSoap version in Craft is to new for kio-extras
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.runtimeDependencies["qt-libs/qcoro"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kactivities"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdnssd"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["kde/applications/libkexiv2"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()
        self.subinfo.options.configure.args += [
            "-DSAMBA_FOUND=false",
            "-DBUILD_KDSoapWSDiscoveryClient=OFF",
        ]  # This requires KDSoap 1.9.0, but we only have a newer version in Craft
