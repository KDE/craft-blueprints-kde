import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/office/skrooge|master"
        self.description = "personal finance manager for KDE"
        self.displayName = "Skrooge"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtsvg"] = None
        self.runtimeDependencies["libs/qt6/qtwebengine"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ktexttemplate"] = None
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["libs/sqlcipher"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.subinfo.options.configure.args = "-DSKG_WEBENGINE=ON"

    def createPackage(self):
        self.defines["executable"] = "bin\\skrooge.exe"  # Windows-only, mac is handled implicitly
        self.defines["icon"] = self.blueprintDir() / "skrooge.ico"
        self.defines["file_types"] = [".skg", ".kmy", ".mny", ".gnucash", ".gsb", ".xhb", ".mmb", ".afb120", ".mt940", ".iif", ".ofx", ".qfx", ".qif", ".csv"]
        self.defines["website"] = "https://skrooge.org/"
        # self.defines["icon"] = self.blueprintDir() / "skrooge.ico"

        return super().createPackage()

