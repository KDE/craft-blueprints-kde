import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.displayName = "Calindori"
        self.description = "Calendar for Plasma Mobile"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kpeople"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/plasma/breeze"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()

    def createPackage(self):
        self.defines["executable"] = r"bin\calindori.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(calindori|update-mime-database|snoretoast)).*")
        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
