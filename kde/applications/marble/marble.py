import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Marble"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt6/qt5compat"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtlocation"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None

        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
            self.runtimeDependencies["libs/protobuf"] = None
            self.runtimeDependencies["libs/qt/qtwebchannel"] = None
            self.runtimeDependencies["libs/qt/qtwebengine"] = None
            self.runtimeDependencies["qt-libs/phonon"] = None
        else:
            self.runtimeDependencies["libs/qt/qtmultimedia"] = None
            self.runtimeDependencies["libs/qt/qtpositioning"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DBUILD_MARBLE_TESTS=OFF"]

    def createPackage(self):
        self.defines["productname"] = "Marble"
        self.defines["executable"] = "bin\\marble-qt.exe"
        self.defines["icon"] = self.sourceDir() / "data/ico/marble.ico"
        self.defines["icon_png"] = self.blueprintDir() / "150-apps-marble.png"
        self.defines["icon_png_44"] = self.blueprintDir() / "44-apps-marble.png"
        self.defines["shortcuts"] = [{"name": "Marble", "target": "bin/marble-qt.exe"}]
        self.defines["website"] = "https://marble.kde.org/"

        self.addExecutableFilter(r"bin/(?!(marble-qt|QtWebEngineProcess)).*")

        return super().createPackage()
