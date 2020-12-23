import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "PIM Addons"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/pim/akonadi-notes"] = None
        self.runtimeDependencies["kde/pim/kcalutils"] = None
        self.runtimeDependencies["kde/pim/kpimtextedit"] = None
        self.runtimeDependencies["kde/pim/kimap"] = None
        self.runtimeDependencies["kde/pim/messagelib"] = None
        self.runtimeDependencies["kde/pim/libkleo"] = None
        self.runtimeDependencies["kde/pim/grantleetheme"] = None
        self.runtimeDependencies["kde/pim/pimcommon"] = None
        self.runtimeDependencies["kde/pim/incidenceeditor"] = None
        self.runtimeDependencies["kde/pim/calendarsupport"] = None
        self.runtimeDependencies["kde/pim/akonadi-calendar"] = None
        self.runtimeDependencies["kde/pim/libgravatar"] = None
        self.runtimeDependencies["kde/pim/kidentitymanagement"] = None
        self.runtimeDependencies["kde/pim/libksieve"] = None
        self.runtimeDependencies["kde/pim/kmailtransport"] = None
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = None
        self.runtimeDependencies["kde/pim/akonadi-import-wizard"] = None
        self.runtimeDependencies["kde/pim/mailimporter"] = None
        self.runtimeDependencies["kde/pim/kpkpass"] = None
        self.runtimeDependencies["kde/pim/kitinerary"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DUSE_UNITY_CMAKE_SUPPORT=ON "
