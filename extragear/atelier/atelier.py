import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'master' ] = 'git://anongit.kde.org/atelier|master'
        self.defaultTarget = 'master'
        self.description = 'Atelier Printer Host'
        self.displayName = "Atelier"

    def setDependencies( self ):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.buildDependencies["kde/frameworks/tier1/solid"] = "default"
        self.buildDependencies["kde/frameworks/tier3/kconfigwidgets"] = "default"
        self.buildDependencies["kde/frameworks/tier3/kxmlgui"] = "default"
        self.buildDependencies["kde/frameworks/tier3/ktexteditor"] = "default"
        self.buildDependencies["extragear/atcore"] = "default"
        self.runtimeDependencies["libs/qt5/qt3d"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtserialport"] = "default"
        self.runtimeDependencies["libs/qt5/qtcharts"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))

    def createPackage(self):
        self.defines[ "executable" ] = "bin\\atelier.exe"
        self.defines[ "version" ] = "1.0"
        self.defines[ "website" ] = "https://atelier.kde.org"
        self.defines[ "icon" ] = os.path.join(self.packageDir(), "atelier.ico")

        return TypePackager.createPackage(self)
