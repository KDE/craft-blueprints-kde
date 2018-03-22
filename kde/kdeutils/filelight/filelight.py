import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "GUI utility to show where your diskspace is being used"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["kdesupport/kdewin"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file.append(os.path.join(os.path.dirname(__file__), 'blacklist.txt'))

    def createPackage(self):
        self.defines["productname"] = "Filelight"
        self.defines["website"] = "https://utils.kde.org/projects/filelight/"
        self.defines["executable"] = "bin\\filelight.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "filelight.ico")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/qt5/qtdeclarative") # pulled in by solid
        self.ignoredPackages.append("kde/frameworks/tier3/kwallet") # pulled in by kio

        return TypePackager.createPackage(self)
