import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Tok"
        self.description = "KDE Telegram client"
        self.webpage = "https://kde.org"
        self.svnTargets["master"] = "https://invent.kde.org/network/tok.git|branch"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/rlottie"] = "default"
        self.runtimeDependencies["libs/td"] = "default"

        if CraftCore.compiler.isMinGW():
            self.runtimeDependencies["libs/runtime"] = None

from Package.CMakePackageBase import * # The package base

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        CMakePackageBase.buildTests = False

    def createPackage(self):
        self.defines["appname"] = "org.kde.Tok"
        self.defines["shortcuts"] = [{"name" : self.subinfo.displayName, "target":"bin/org.kde.Tok.exe"}]

        return super().createPackage()