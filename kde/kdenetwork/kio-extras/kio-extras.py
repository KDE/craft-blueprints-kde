import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Extra plugins for KIO (thumbnail generators, archives, remote filesystems and more)"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/libssh"] = None
        self.runtimeDependencies["libs/openexr"] = None
        self.runtimeDependencies["libs/taglib"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        # self.runtimeDependencies["qt-libs/kdsoap"] = None # Our KDSoap version in Craft is too new for kio-extras
        self.runtimeDependencies["qt-libs/qcoro"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/plasma/plasma-activities"] = None
        self.runtimeDependencies["kde/plasma/plasma-activities-stats"] = None
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DSAMBA_FOUND=false",
            "-DBUILD_KDSoapWSDiscoveryClient=OFF",
        ]  # This requires KDSoap 1.9.0, but we only have a newer version in Craft

        self.subinfo.options.configure.args += [f"-DBUILD_ACTIVITIES={self.subinfo.options.isActive('kde/plasma/plasma-activities-stats').asOnOff}"]
        # TODO: we don't have libproxy in Craft yet
        self.subinfo.options.configure.args += ["-DWITH_LIBPROXY=OFF"]
