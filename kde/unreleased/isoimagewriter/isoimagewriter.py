import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Packager.AppImagePackager import AppImagePackager


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.svnTargets["master"] = "https://invent.kde.org/utilities/isoimagewriter.git"
        for ver in ["1.0.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/isoimagewriter/{ver}/isoimagewriter-{ver}.tar.xz"
            self.targetInstSrc[ver] = "isoimagewriter-{ver}"
        self.defaultTarget = "1.0.0"

        self.displayName = "ISO Image Writer"
        self.description = "A tool to write ISO images to USB flash drives"

    def setDependencies(self):
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isWindows:
            manifest = self.sourceDir() / "res/isoimagewriter.manifest"
            app = self.installDir(), "bin/isoimagewriter.exe"
            self.addExecutableFilter(r"bin/(?!(isoimagewriter|update-mime-database|kioslave)).*")
            return utils.embedManifest(app, manifest)
        if CraftCore.compiler.isLinux and isinstance(self, AppImagePackager):
            utils.copyFile(
                CraftCore.standardDirs.craftRoot() / "share/icons/breeze/devices/64/drive-removable-media.svg",
                self.installDir() / "share/breeze/apps/64/drive-removable-media.svg",
            )

        return True

    def createPackage(self):
        self.defines["shortcuts"] = [{"name": "KDE ISO Image Writer", "target": "bin/isoimagewriter.exe", "description": self.subinfo.description}]
        self.defines["icon"] = self.blueprintDir() / "isoimagewriter.ico"
        return super().createPackage()
