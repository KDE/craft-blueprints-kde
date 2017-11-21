import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Marble"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt5/qtconcurrent"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qt5/qtnetwork"] = "default"
        self.runtimeDependencies["libs/qt5/qtsvg"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier3/kconfigwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcrash"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["frameworks/tier3/knewstuff"] = "default"
        self.runtimeDependencies["frameworks/tier3/kparts"] = "default"
        self.runtimeDependencies["frameworks/tier3/krunner"] = "default"
        self.runtimeDependencies["frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["frameworks/tier3/kwallet"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
