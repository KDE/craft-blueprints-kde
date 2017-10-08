import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Kig"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt5/qtgui"] = "default"
        self.runtimeDependencies["libs/qt5/qtprintsupport"] = "default"
        self.runtimeDependencies["libs/qt5/qtsvg"] = "default"
        self.runtimeDependencies["libs/qt5/qtwidgets"] = "default"
        self.runtimeDependencies["libs/qt5/qtxml"] = "default"
        self.runtimeDependencies["frameworks/tier1/karchive"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier3/kconfigwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcrash"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/tier3/kparts"] = "default"
        self.runtimeDependencies["frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
