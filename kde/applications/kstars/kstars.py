import info
import os
import subprocess

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        
        self.description = 'a desktop planetarium'
        self.svnTargets['3.5.6'] = 'https://invent.kde.org/education/kstars.git|stable-3.5.6'
        self.svnTargets['master'] = "https://github.com/KDE/kstars.git"
        self.defaultTarget = 'master'
        self.displayName = "KStars Desktop Planetarium"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qtdatavis3d"] = None
        self.runtimeDependencies["libs/qt5/qtwebsockets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpackage"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kinit"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kplotting"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["libs/eigen3"] = None
        self.runtimeDependencies["libs/cfitsio"] = None
        self.runtimeDependencies["libs/wcslib"] = None

        if CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/_mac/xplanet"] = None
            self.runtimeDependencies["libs/_mac/gsc"] = None
            #Making these dependencies casues an issue where you can't have KStars and INDI both be the latest version or both be stable
            #You have to comment these out if you want stable, this basically hard codes it to be the latest version.
            self.runtimeDependencies["libs/_mac/indiserver"] = None
            self.runtimeDependencies["libs/_mac/indiserver-3rdparty"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/indiclient"] = None

        self.runtimeDependencies["libs/libraw"] = None
        self.runtimeDependencies["libs/gsl"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/stellarsolver"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None

        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["qt-libs/phonon-vlc"] = None
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/llvm-meta")
        if CraftCore.compiler.isWindows:
            self.blacklist_file = ["win-blacklist.txt"]
        if CraftCore.compiler.isMacOS:
            self.blacklist_file = ["mac-blacklist.txt"]
        self.subinfo.options.configure.args += "-DBUILD_DOC=OFF"

    def make(self):
        if not super().make():
            return False

        if not CraftCore.compiler.isMacOS:
            return True

        #	Copying things needed for MacOS KStars

        #	Defining Craft Directories
        buildDir = str(self.buildDir())
        sourceDir = str(self.sourceDir())
        packageDir = str(self.packageDir())
        imageDir = str(self.imageDir())
        craftRoot = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(craftRoot,  'lib')
        KSTARS_APP = os.path.join(buildDir , 'bin' , 'KStars.app')
        KSTARS_RESOURCES = os.path.join(KSTARS_APP , 'Contents' , 'Resources')
        KSTARS_PLUGINS = os.path.join(KSTARS_APP , 'Contents' , 'PlugIns')

		# INDI Related items

        #	INDI Drivers
        utils.system("cp -f " + craftRoot + "/bin/indi* " + KSTARS_APP + "/Contents/MacOS/")

        #	INDI firmware files"
        utils.system("mkdir -p " + KSTARS_RESOURCES + "/DriverSupport/")
        utils.system("cp -rf " + craftRoot + "/usr/local/lib/indi/DriverSupport " + KSTARS_RESOURCES)

        #	Driver XML Files
        utils.system("cp -f " + craftRoot + "/share/indi/* " + KSTARS_RESOURCES + "/DriverSupport/")

        #	Math Plugins
        utils.system("cp -rf " + craftRoot + "/lib/indi/MathPlugins " + KSTARS_RESOURCES)

        #	The gsc executable
        utils.system("cp -f " + craftRoot + "/bin/gsc " + KSTARS_APP + "/Contents/MacOS/")

        #	GPhoto Plugins
        GPHOTO_VERSION = subprocess.getoutput("pkg-config --modversion libgphoto2")
        PORT_VERSION = "0.12.0"
        utils.system("mkdir -p " + KSTARS_RESOURCES + "/DriverSupport/gphoto/IOLIBS")
        utils.system("mkdir -p " + KSTARS_RESOURCES + "/DriverSupport/gphoto/CAMLIBS")
        utils.system("cp -rf " + craftRoot + "/lib/libgphoto2_port/" + PORT_VERSION + "/* " + KSTARS_RESOURCES + "/DriverSupport/gphoto/IOLIBS/")
        utils.system("cp -rf " + craftRoot + "/lib/libgphoto2/" + GPHOTO_VERSION + "/* " + KSTARS_RESOURCES + "/DriverSupport/gphoto/CAMLIBS/")

        # Qt Related items

        #	The Translations Directory
        utils.system("cp -rf " + craftRoot + "/share/locale " + KSTARS_RESOURCES)

        #   Plugins
        utils.system("cp -rf " + craftRoot + "/plugins/* " + KSTARS_PLUGINS)

        # qt.conf
        confContents = "[Paths]\n"
        confContents += "Prefix = " + craftRoot + "\n"
        confContents += "Plugins = plugins\n"
        confContents += "Imports = qml\n"
        confContents += "Qml2Imports = qml\n"
        confContents += "Translations = " + craftRoot + "/share/locale\n"

        utils.system("touch " + KSTARS_RESOURCES + "/qt.conf")
        utils.system("echo \"" + confContents + "\" >> " + KSTARS_RESOURCES + "/qt.conf")

        for path in utils.getLibraryDeps(str(KSTARS_APP + "/Contents/MacOS/kstars")):
            if path.startswith(craftLibDir):
                utils.system(["install_name_tool", "-change", path, os.path.join("@rpath", os.path.basename(path)), KSTARS_APP + "/Contents/MacOS/kstars"])

        return True

    def createPackage(self):
        self.defines["executable"] = "bin\\kstars.exe"
        #self.defines["setupname"] = "kstars-latest-win64.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kstars.ico")
        # TODO: support dpi scaling
        # TODO: use assets from src with the next release
        #self.defines["icon_png"] = os.path.join(self.sourceDir(), "packaging", "windows", "assets", "Square150x150Logo.scale-100.png")
        #self.defines["icon_png_44"] = os.path.join(self.sourceDir(), "packaging", "windows", "assets", "Square44x44Logo.scale-100.png")
        #self.defines["icon_png_310x150"] = os.path.join(self.sourceDir(), "packaging", "windows", "assets", "Wide310x150Logo.scale-100.png")
        #self.defines["icon_png_310x310"] = os.path.join(self.sourceDir(), "packaging", "windows", "assets", "Square310x310Logo.scale-100.png")
        self.defines["icon_png"] = os.path.join(self.packageDir(), ".assets", "Square150x150Logo.scale-100.png")
        self.defines["icon_png_44"] = os.path.join(self.packageDir(), ".assets", "Square44x44Logo.scale-100.png")
        self.defines["icon_png_310x150"] = os.path.join(self.packageDir(), ".assets", "Wide310x150Logo.scale-100.png")
        self.defines["icon_png_310x310"] = os.path.join(self.packageDir(), ".assets", "Square310x310Logo.scale-100.png")
        if isinstance(self, AppxPackager):
              self.defines["display_name"] = "KStars"

        return TypePackager.createPackage(self)
