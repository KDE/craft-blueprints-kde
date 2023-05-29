import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "KolourPaint is an easy-to-use paint program"
        self.displayName = "Kolourpaint"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file.append(os.path.join(os.path.dirname(__file__), "blacklist.txt"))

    def createPackage(self):
        self.defines["executable"] = "bin\\kolourpaint.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kolourpaint.ico")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("kde/frameworks/kdesignerplugin")
        self.ignoredPackages.append("kde/frameworks/kemoticons")

        return TypePackager.createPackage(self)
