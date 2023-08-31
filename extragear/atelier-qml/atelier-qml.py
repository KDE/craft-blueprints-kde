import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/laysrodrigues/atelier-qml.git"
        self.defaultTarget = "master"
        self.description = "Atelier Printer Host QML-Version"
        self.webpage = "https://atelier.kde.org"
        self.displayName = "Atelier"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["extragear/atcore"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtserialport"] = None
        self.runtimeDependencies["libs/qt/qtcharts"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist.txt"))
        self.defines["executable"] = "bin\\atelier.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "atelier.ico")

        return super().createPackage()
