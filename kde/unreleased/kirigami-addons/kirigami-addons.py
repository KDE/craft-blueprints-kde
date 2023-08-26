import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/kirigami-addons.git"
        self.defaultTarget = "0.11.0"

        for ver in ["0.11.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/kirigami-addons/kirigami-addons-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/kirigami-addons/kirigami-addons-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = "kirigami-addons-" + ver

        self.description = "Addons for the Kirigami Framework"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def init(self):
        CMakePackageBase.init(self)
