import info
from Packager.CollectionPackagerBase import PackagerLists


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Umbrello is a UML modelling application."
        self.displayName = "Umbrello"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/dbus"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtwebkit"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kauth"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier4/kdelibs4support"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        # for php support
        self.runtimeDependencies["extragear/kdevelop-pg-qt"] = None
        self.runtimeDependencies["extragear/kdevelop/kdev-php"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [PackagerLists.runtimeBlacklist, os.path.join(os.path.dirname(__file__), "blacklist.txt")]

    def createPackage(self):
        self.defines["executable"] = "bin\\umbrello5.exe"
        # self.defines["icon"] = os.path.join(self.packageDir(), "umbrello.ico")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("dev-utils/sed")
        self.ignoredPackages.append("kde/frameworks/kdesignerplugin")
        self.ignoredPackages.append("kde/frameworks/kemoticons")

        return TypePackager.createPackage(self)
