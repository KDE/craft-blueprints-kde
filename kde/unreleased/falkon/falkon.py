import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        # NOTE: As of 25.04.1, no Windows compatible official release, yet
        self.svnTargets["master"] = "https://invent.kde.org/network/falkon.git"
        self.defaultTarget = "master"

        self.description = "Cross-platform Qt web-browser"
        self.displayName = "Falkon"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtwebengine"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        # NOTE: Should depend on pyside6, shiboken6, shiboken6tools, once available


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.defines["executable"] = "bin\\falkon.exe"
        self.defines["file_types"] = [".HTML", ".HTML"]
        # NOTE: Would like to register http:// and https:// protocols, too

        self.ignoredPackages.append("binary/mysql")

        return super().createPackage()
