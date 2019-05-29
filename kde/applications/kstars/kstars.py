import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = 'a desktop planetarium'
        for ver in ['3.2.3']:
            self.targets[ver] = 'http://download.kde.org/stable/kstars/kstars-%s.tar.xz' % ver
            self.targetInstSrc[ver] = 'kstars-%s' % ver
        self.defaultTarget = '3.2.3'
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
        self.runtimeDependencies["libs/indiclient"] = None
        self.runtimeDependencies["libs/libraw"] = None
        self.runtimeDependencies["libs/gsl"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None

        # Install proper theme
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None

        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["qt-libs/phonon-vlc"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/llvm-meta")
        self.blacklist_file = ["blacklist.txt"]

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
