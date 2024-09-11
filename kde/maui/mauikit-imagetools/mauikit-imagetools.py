import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/maui/mauikit-imagetools.git"

        for ver in ["2.1.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/maui/mauikit-imagetools/{ver}/mauikit-imagetools-{ver}.tar.xz"
            self.archiveNames[ver] = f"mauikit-imagetools-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"mauikit-imagetools-{ver}"

        self.description = "MauiKit Image utilities and controls"
        self.defaultTarget = "2.1.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/exiv2"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/maui/mauikit"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
