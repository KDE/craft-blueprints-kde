import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl = "https://invent.kde.org/utilities/kongress.git")
        self.displayName = "Kongress"
        self.description = "Conference companion app"

        self.patchToApply["21.05"] = [("0001-Build-without-DBus-on-Android.patch", 1),
                                      ("0002-Use-QGuiApplication-on-Android.patch", 1),
                                      ("0003-Use-QGuiApplication-instead-of-QApplication-where-po.patch", 1)]
        self.patchLevel["21.05"] = 1

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/plasma/breeze"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["executable"] = r"bin\kongress.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(kongress|update-mime-database|snoretoast)).*")
        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
