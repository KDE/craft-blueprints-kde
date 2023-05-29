import info
import utils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Cantor"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = None
        self.runtimeDependencies['libs/qt5/qtwebengine'] = None
        self.runtimeDependencies["libs/qt5/qttools"] = None
        self.runtimeDependencies["qt-libs/poppler"] = None
        # required on macOS
        if CraftCore.compiler.isMacOS:
            self.runtimeDependencies['libs/expat'] = None
            self.runtimeDependencies["libs/webp"] = None
        # libR.dylib fails packaging on macOS (lapack.so)
        if not CraftCore.compiler.isMacOS:
            if OsUtils.isWin():
                self.runtimeDependencies["binary/r-base"] = None
            else:
                self.runtimeDependencies["libs/r-base"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpty"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/applications/analitza"] = None

from Package.CMakePackageBase import *
from Packager.AppxPackager import AppxPackager


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        #if CraftCore.compiler.isWindows:
            #self.subinfo.options.make.supportsMultijob = False

            # R backend fail compiling on Windows
            #self.r_dir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "bin", "x64")
            #self.subinfo.options.configure.args = "-DR_EXECUTABLE=" + OsUtils.toUnixPath(os.path.join(self.r_dir, "R.exe"))
            #self.subinfo.options.configure.args += " -DR_R_LIBRARY=" + OsUtils.toUnixPath(os.path.join(self.r_dir, "R.dll"))

            #pythonPath = CraftCore.settings.get("Paths", "PYTHON")
            #self.subinfo.options.configure.args += f" -DPYTHONLIBS3_LIBRARY=\"{pythonPath}\libs\python38.lib\" -DPYTHONLIBS3_INCLUDE_DIR=\"{pythonPath}\include\""

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        # Some plugins files break code signing on macOS, which is picky about file names
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist_mac.txt'))

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")

        self.defines["appname"] = "cantor"
        self.defines["website"] = "https://cantor.kde.org/"
        self.defines["executable"] = "bin\\cantor.exe"
        self.defines["shortcuts"] = [{"name" : "Cantor", "target" : "bin/cantor.exe", "description" : self.subinfo.description, "icon" : "$INSTDIR\\cantor.ico" }]
        self.defines["icon"] = os.path.join(self.packageDir(), "cantor.ico")
        if self.buildTarget == "master":
            self.defines["icon_png"] = os.path.join(self.sourceDir(), "icons", "150-apps-cantor.png")
            self.defines["icon_png_44"] = os.path.join(self.sourceDir(), "icons", "44-apps-cantor.png")
            self.defines["icon_png_310"] = os.path.join(self.sourceDir(), "icons", "310-apps-cantor.png")

        if isinstance(self, AppxPackager):
            self.defines["display_name"] = "Cantor"

        # see labplot.py for more
 
        return TypePackager.createPackage(self)
