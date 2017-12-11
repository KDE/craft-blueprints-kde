import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.41.0"] = [("0001-Check-for-Linux-instead-of-TagLib-and-avoid-building.patch", 1),
                                       ("0003-Fix-build-against-TagLib-1.11.patch", 1)]

        self.description = "A file metadata and text extraction library"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"

        self.runtimeDependencies["frameworks/tier1/karchive"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"

        # self.runtimeDependencies["qt-libs/poppler"] = "default"
        self.runtimeDependencies["win32libs/taglib"] = "default"
        self.runtimeDependencies["win32libs/exiv2"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
