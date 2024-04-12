import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/maui/mauikit-accounts.git"

        for ver in ["2.1.0"]:
            self.targets[ver] = "https://download.kde.org/stable/maui/mauikit-accounts/%s/mauikit-accounts-%s.tar.xz" % (ver, ver)
            self.archiveNames[ver] = "mauikit-accounts-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "mauikit-accounts-%s" % ver

        self.description = "MauiKit accounts"
        self.defaultTarget = "2.1.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/maui/mauikit"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
