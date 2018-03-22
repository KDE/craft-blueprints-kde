import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "MailCommon library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = "default"

        self.runtimeDependencies["kde/pim/akonadi"] = "default"
        self.runtimeDependencies["kde/pim/akonadi-mime"] = "default"
        self.runtimeDependencies["kde/pim/messagelib"] = "default"
        self.runtimeDependencies["kde/pim/kmailtransport"] = "default"
        self.runtimeDependencies["kde/pim/mailimporter"] = "default"
        self.runtimeDependencies["kde/pim/kmime"] = "default"
        self.runtimeDependencies["kde/pim/pimcommon"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
