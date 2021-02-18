import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.displayName = "Kate"
        self.description = "the KDE text editor"
        self.webpage = "https://kate-editor.org/"

    def registerOptions(self):
        self.options.dynamic.registerOption("fullPlasma", False)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kactivities"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kinit"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        if self.options.dynamic.fullPlasma:
            self.runtimeDependencies["kde/frameworks/tier3/plasma-framework"] = None
        if OsUtils.isUnix():
            self.runtimeDependencies["kde/applications/konsole"] = None

        # KUserFeedback yet not an official tier1 framework
        self.runtimeDependencies["kde/unreleased/kuserfeedback"] = None

        # try to use Breeze style as Windows style has severe issues for e.g. scaling
        self.runtimeDependencies["kde/plasma/breeze"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if not self.subinfo.options.dynamic.fullPlasma:
            self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_KF5Plasma=ON"

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist_mac.txt'))
        self.addExecutableFilter(r"bin/(?!(kate|update-mime-database|kioslave)).*")
        self.defines["shortcuts"] = [{"name" : "Kate", "target":"bin/kate.exe", "description" : self.subinfo.description}]

        # kate icons
        self.defines["icon"] = self.buildDir() / "kate/ICONS_SOURCES.ico"

        # support new special windows icons, if there (>= 21.04)
        if os.path.join(self.sourceDir(), "kate", "icons", "windows", "150-apps-kate.png").exists():
            self.defines["icon_png"] = os.path.join(self.sourceDir(), "kate", "icons", "windows", "150-apps-kate.png")
            self.defines["icon_png_44"] = os.path.join(self.sourceDir(), "kate", "icons", "windows", "44-apps-kate.png")
        else:
            self.defines["icon_png"] = os.path.join(self.sourceDir(), "kate", "icons", "150-apps-kate.png")
            self.defines["icon_png_44"] = os.path.join(self.sourceDir(), "kate", "icons", "44-apps-kate.png")

        # this requires an 310x150 variant in addition!
        #self.defines["icon_png_310x310"] = os.path.join(self.sourceDir(), "kate", "icons", "310-apps-kate.png")

        self.defines["registry_hook"] = ("""WriteRegStr SHCTX "Software\\Classes\\*\\shell\\EditWithKate" "" "Edit with Kate"\n"""
                                        """WriteRegStr SHCTX "Software\\Classes\\*\\shell\\EditWithKate\\command" "" '"$INSTDIR\\bin\\kate.exe" "%V"'\n""")

        self.defines["mimetypes"] = ["text/plain", "text/html", "text/xml", "text/css", "text/csv", "application/json", "application/xml", "application/javascript"]
        self.defines["file_types"] = [".ini", ".conf", ".cfg", ".cpp", ".hpp", ".py", ".yaml", ".toml", ".log", ".md"]

        self.defines["alias"] = "kate"

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        return TypePackager.createPackage(self)
