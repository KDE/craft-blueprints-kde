import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.defaultTarget = "master"

        self.description = "Compares and merges 2 or 3 files or directories"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/boost/boost-headers"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
    def createPackage(self):
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist_mac.txt'))
        
        self.defines["executable"] = "bin\\kdiff3.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kdiff3.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
