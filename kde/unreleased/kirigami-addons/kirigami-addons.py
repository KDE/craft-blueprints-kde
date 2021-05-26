import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://anongit.kde.org/kirigami-addons.git'
        self.defaultTarget = '0.2'

        self.targets["0.2"] = "https://download.kde.org/unstable/kirigami-addons/0.2/kirigami-addons-0.2.tar.xz"
        self.targetDigestUrls["0.2"] = "https://download.kde.org/unstable/kirigami-addons/0.2/kirigami-addons-0.2.tar.xz.sha256"
        self.targetInstSrc["0.2"] = "kirigami-addons-0.2"

        self.description = "Addons for the Kirigami Framework"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def init(self):
        CMakePackageBase.init(self)
