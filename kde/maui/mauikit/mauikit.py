import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/maui/mauikit.git"

        for ver in ["2.1.0"]:
            self.targets[ver] = "https://download.kde.org/stable/maui/mauikit/%s/mauikit-%s.tar.xz" % (ver, ver)
            self.archiveNames[ver] = "mauikit-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "mauikit-%s" % ver

        self.description = "Templated convergent controls and multi-platform utilities for Maui applications"
        self.defaultTarget = "2.1.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
