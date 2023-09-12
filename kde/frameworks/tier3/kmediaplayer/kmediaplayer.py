import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(
            tarballUrl="https://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/${PACKAGE_NAME}-${VERSION}.tar.xz",
            tarballDigestUrl="https://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/${PACKAGE_NAME}-${VERSION}.tar.xz.sha1",
        )

        self.description = "Plugin interface for media player features"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
