import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/office/skrooge|master"
        self.description = "personal finance manager for KDE"
        self.displayName = "Skrooge"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qt5compat"] = None
        self.runtimeDependencies["libs/sqlcipher"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ktexttemplate"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt6/qtwebengine"] = None
            self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
            self.runtimeDependencies["libs/qt6/qtsvg"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
            self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        else:
            self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
            self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.subinfo.options.configure.args = "-DSKG_WEBENGINE=ON"

    def createPackage(self):
        self.defines["executable"] = "bin\\skrooge.exe"  # Windows-only, mac is handled implicitly
        self.defines["icon"] = self.blueprintDir() / "skrooge.ico"
        self.defines["file_types"] = [".skg", ".kmy", ".mny", ".gnucash", ".gsb", ".xhb", ".mmb", ".afb120", ".mt940", ".iif", ".ofx", ".qfx", ".qif", ".csv"]
        self.defines["website"] = "https://skrooge.org/"
        # self.defines["icon"] = self.blueprintDir() / "skrooge.ico"

        # Correctif macOS : Réparation du chemin durci de qca-qt6 issu des binaires pré-compilés du CI
        if CraftCore.compiler.isMacOS:
            ksecretd_path = self.imageDir() / "bin" / "ksecretd"
            if not ksecretd_path.exists():
                ksecretd_path = CraftCore.standardDirs.craftRoot() / "bin" / "ksecretd"

            if ksecretd_path.exists():
                old_path = "/Users/gitlab/builds/GZwHuM5xu/0/sysadmin/craft-ci/macos-64-clang/lib/qca-qt6.framework/Versions/2/qca-qt6"
                new_path = "@rpath/qca-qt6.framework/Versions/2/qca-qt6"
                utils.system(["install_name_tool", "-change", old_path, new_path, str(ksecretd_path)], ignoreSuccess=True)

        return super().createPackage()
