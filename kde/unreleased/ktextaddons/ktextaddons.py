import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://invent.kde.org/libraries/ktextaddons.git'
        self.defaultTarget = '1.0'

        for ver in ['1.0']:
            self.targets[ ver ] = f"https://download.kde.org/stable/ktextaddons/ktextaddons-{ver}.tar.xz"
            self.targetDigestUrls[ ver ] = f"https://download.kde.org/stable/ktextaddons/ktextaddons-{ver}.tar.xz.sha256"
            self.targetInstSrc[ ver ] = "ktextaddons-" + ver

        self.description = "Various text handling addons"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def init(self):
        CMakePackageBase.init(self)
