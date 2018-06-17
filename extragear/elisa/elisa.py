import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues()
        self.targets['0.1.0'] = 'https://download.kde.org/stable/elisa/0.1/elisa-0.1.tar.xz'
        self.targetDigestUrls['0.1.0'] = 'https://download.kde.org/stable/elisa/0.1/elisa-0.1.tar.xz.sha256'
        self.targetInstSrc['0.1.0'] = 'elisa-0.1'

        self.targets['0.1.80'] = 'https://download.kde.org/unstable/elisa/0.1.80/elisa-0.1.80.tar.xz'
        self.targetDigestUrls['0.1.80'] = 'https://download.kde.org/unstable/elisa/0.1.80/elisa-0.1.80.tar.xz.sha256'
        self.targetInstSrc['0.1.80'] = 'elisa-0.1.80'

        self.defaultTarget = '0.1.80'

        self.displayName = "Elisa"
        self.description = "the Elisa music player"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtgraphicaleffects"] = "default"
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = "default"
        self.runtimeDependencies["libs/qt5/qtquickcontrols"] = "default"
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = "default"
        self.runtimeDependencies["libs/qt5/qtsvg"] = "default"
        self.runtimeDependencies["libs/qt5/qtwinextras"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kfilemetadata"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["executable"] = "bin\\elisa.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "elisa.ico")

        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")

        return TypePackager.createPackage(self)
