import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in ['5.37.0', '5.38.0']:
            self.patchToApply[ver] = [("0001-fix-crash-when-more-than-one-instances-of-ExtractorC.patch", 1)]

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
