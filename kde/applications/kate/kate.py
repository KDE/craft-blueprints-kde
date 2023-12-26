import info
from CraftOS.osutils import OsUtils
from Packager.AppImagePackager import AppImagePackager

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

        # KUserFeedback yet not an official tier1 framework
        self.runtimeDependencies["kde/unreleased/kuserfeedback"] = None

        # try to use Breeze style as Windows style has severe issues for e.g. scaling
        self.runtimeDependencies["kde/plasma/breeze"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def setDefaults(self, defines: {str: str}) -> {str: str}:
        defines = super().setDefaults(defines)
        if OsUtils.isLinux() and isinstance(self, AppImagePackager):
            defines["runenv"] += [
                "LD_LIBRARY_PATH=$this_dir/usr/lib/:$LD_LIBRARY_PATH",
            ]
        return defines

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist.txt"))
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist_mac.txt"))
        self.addExecutableFilter(r"bin/(?!(kate|update-mime-database|kioslave)).*")
        self.defines["shortcuts"] = [{"name": "Kate", "target": "bin/kate.exe", "description": self.subinfo.description}]

        # kate icons
        self.defines["icon"] = self.buildDir() / "apps/kate/ICONS_SOURCES.ico"

        # use special windows icons
        self.defines["icon_png"] = os.path.join(self.sourceDir(), "apps", "kate", "icons", "windows", "150-apps-kate.png")
        self.defines["icon_png_44"] = os.path.join(self.sourceDir(), "apps", "kate", "icons", "windows", "44-apps-kate.png")

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
        self.defines["file_types"] = [".ini", ".conf", ".cfg", ".cpp", ".hpp", ".py", ".yaml", ".toml", ".log", ".md"]

        self.defines["alias"] = "kate"

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        return TypePackager.createPackage(self)
