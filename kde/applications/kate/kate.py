import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.displayName = "Kate"
        self.description = "Modern text editor built on the KDE Frameworks and Qt"
        self.webpage = "https://kate-editor.org/"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/kdeutils/markdownpart"] = None
        self.runtimeDependencies["kde/applications/konsole"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kuserfeedback"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None

        # try to use Breeze style as Windows style has severe issues for e.g. scaling
        self.runtimeDependencies["kde/plasma/breeze"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.addExecutableFilter(r"(bin|libexec)/(?!(kate|update-mime-database|kioworker)).*")

        self.defines["shortcuts"] = [{"name": "Kate", "target": "bin/kate.exe", "description": self.subinfo.description}]

        # kate icons
        self.defines["icon"] = self.buildDir() / "apps/kate/ICONS_SOURCES.ico"

        # use special windows icons
        self.defines["icon_png"] = self.sourceDir() / "apps/kate/icons/windows/150-apps-kate.png"
        self.defines["icon_png_44"] = self.sourceDir() / "apps/kate/icons/windows/44-apps-kate.png"

        self.defines["registry_hook"] = (
            """WriteRegStr SHCTX "Software\\Classes\\*\\shell\\EditWithKate" "" "Edit with Kate"\n"""
            """WriteRegStr SHCTX "Software\\Classes\\*\\shell\\EditWithKate\\command" "" '"$INSTDIR\\bin\\kate.exe" "%V"'\n"""
        )

        self.defines["mimetypes"] = [
            "text/plain",
            "text/html",
            "text/xml",
            "text/css",
            "text/csv",
            "application/json",
            "application/xml",
            "application/javascript",
        ]
        self.defines["file_types"] = [".txt", ".ini", ".conf", ".cfg", ".cpp", ".hpp", ".py", ".yaml", ".toml", ".log", ".md"]

        self.defines["alias"] = "kate"

        # skip some dependencies we don't need during runtime
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/llvm")

        # skip dbus for macOS and Windows, we don't use it there and it only leads to issues
        if not CraftCore.compiler.platform.isLinux:
            self.ignoredPackages.append("libs/dbus")

        return super().createPackage()
