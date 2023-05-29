import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/office/kile.git"
        self.svnTargets["gitStable-2.1"] = "https://invent.kde.org/office/kile.git"
        for ver in ["2.1.1", "2.9.92", "2.9.93"]:
            self.targets[ver] = "http://downloads.sourceforge.net/kile/kile-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = "kile-" + ver
        self.description = "a user friendly TeX/LaTeX editor for KDE"
        self.displayName = "Kile"
        self.webpage = "https://kile.sourceforge.io/"
        self.defaultTarget = "2.9.93"
        self.patchToApply["2.9.93"] = [("kile-disable-sonnet-language-autodetect.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtscript"] = None
        self.runtimeDependencies["qt-libs/poppler"] = None
        self.runtimeDependencies["kde/applications/okular"] = None
        self.runtimeDependencies["kde/applications/kate"] = None
        self.runtimeDependencies["kde/frameworks/tier3/khtml"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist.txt"))
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist_mac.txt"))
        self.defines["executable"] = "bin\\kile.exe"

        # kile icons
        self.defines["icon"] = os.path.join(self.packageDir(), "kile.ico")
        self.defines["icon_png"] = os.path.join(self.sourceDir(), "src", "data", "icons", "150-apps-kile.png")
        self.defines["icon_png_44"] = os.path.join(self.sourceDir(), "src", "data", "icons", "44-apps-kile.png")

        # this requires an 310x150 variant in addition!
        # self.defines["icon_png_310x310"] = os.path.join(self.sourceDir(), "src", "data", "icons", "310-apps-kile.png")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
