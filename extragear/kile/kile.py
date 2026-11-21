import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/office/kile.git"
        self.svnTargets["gitStable-2.1"] = "https://invent.kde.org/office/kile.git"
        for ver in ["2.1.1", "2.9.92", "2.9.93"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/kile/kile-{ver}.tar.bz2"
            self.targetInstSrc[ver] = "kile-" + ver
        self.description = "a user friendly TeX/LaTeX editor for KDE"
        self.displayName = "Kile"
        self.webpage = "https://kile.sourceforge.io/"
        self.defaultTarget = "2.9.93"
        self.patchToApply["2.9.93"] = [("kile-disable-sonnet-language-autodetect.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["qt-libs/poppler"] = None
        self.runtimeDependencies["kde/applications/okular"] = None
        self.runtimeDependencies["kde/applications/kate"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        if CraftCore.compiler.platform.isMacOS:
            self.blacklist_file.append(self.blueprintDir() / "blacklist_mac.txt")
        self.defines["executable"] = "bin\\kile.exe"

        # kile icons
        self.defines["icon"] = self.blueprintDir() / "kile.ico"
        self.defines["icon_png"] = self.sourceDir() / "src/data/icons/150-apps-kile.png"
        self.defines["icon_png_44"] = self.sourceDir() / "src/data/icons/44-apps-kile.png"

        # this requires a 310x150 variant in addition!
        # self.defines["icon_png_310x310"] = os.path.join(self.sourceDir(), "src", "data", "icons", "310-apps-kile.png")

        self.ignoredPackages.append("binary/mysql")

        return super().createPackage()
