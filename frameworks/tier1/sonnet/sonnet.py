import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.41.0"] = [("0001-Don-t-cause-circular-linking-on-Windows.patch", 1),
                                       ("0001-Remove-anchient-and-broken-workaround.patch", 1)]
        self.patchLevel["5.41.0"] = 2

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
