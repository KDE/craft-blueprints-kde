import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Umbrello is a UML modelling application."
        self.displayName = "Umbrello"

    def registerOptions(self):
        self.options.dynamic.registerOption("buildPHPImport", True)

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/dbus"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtwebengine"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kauth"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None

        if self.options.dynamic.buildPHPImport:
            # for php support
            self.runtimeDependencies["extragear/kdevelop-pg-qt"] = None
            self.runtimeDependencies["extragear/kdevelop/kdev-php"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [f"-DBUILD_PHP_IMPORT={'ON' if self.subinfo.options.dynamic.buildPHPImport else 'OFF'}"]
        if not CraftCore.compiler.isMacOS:
            self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")

    def createPackage(self):
        self.addExecutableFilter(
            r"bin/(?!(dbus-daemon|dbus-send|dbus-monitor|dbus-launch|qdbus|qdbusviewer|kbuildsycoca5|umbrello|update-mime-database|kioworker)).*"
        )
        self.defines["appname"] = "umbrello5"
        self.defines["executable"] = "bin\\umbrello5.exe"
        # self.defines["icon"] = os.path.join(self.blueprintDir(), "umbrello.ico")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("dev-utils/sed")
        return super().createPackage()
