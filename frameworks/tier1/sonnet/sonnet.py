import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.43.0"] = [("0001-Find-libhunspell-build-by-msvc.patch", 1),
                                       ("0002-Use-Locale-name-instead-of-Locale-bcp47Name.patch", 1)]
        self.patchLevel["5.43.0"] = 1

        self.description = "Spelling framework for Qt, plugin-based."

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["win32libs/aspell"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
