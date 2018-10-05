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

        self.targets['0.2.80'] = 'https://download.kde.org/unstable/elisa/0.2.80/elisa-0.2.80.tar.xz'
        self.targetDigestUrls['0.2.80'] = 'https://download.kde.org/unstable/elisa/0.2.80/elisa-0.2.80.tar.xz.sha256'
        self.targetInstSrc['0.2.80'] = 'elisa-0.2.80'

        self.defaultTarget = '0.3'

        self.displayName = "Elisa"
        self.description = "the Elisa music player"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtgraphicaleffects"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qtwinextras"] = None
        self.runtimeDependencies["binary/vlc"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kfilemetadata"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None

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
