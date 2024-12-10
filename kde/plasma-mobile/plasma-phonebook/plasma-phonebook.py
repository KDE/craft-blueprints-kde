import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.displayName = "Plasma Phonebook"
        self.description = "Phonebook for Plasma Mobile"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcontacts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kpeople"] = None
        self.runtimeDependencies["kde/pim/kpeoplevcard"] = None
        self.runtimeDependencies["kde/libs/kirigami-addons"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/plasma/breeze"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.defines["executable"] = r"bin\plasma-phonebook.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(plasma-phonebook|update-mime-database|snoretoast)).*")
        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
