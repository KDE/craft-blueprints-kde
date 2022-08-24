import info
from Blueprints.CraftVersion import CraftVersion


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets[ 'master' ] = 'https://anongit.kde.org/calligra.git'
        self.defaultTarget = 'master'
        self.description = 'The Integrated Work Applications Suite by KDE'
        self.webpage = "https://calligra.org/"
        self.displayName = "Calligra Gemini"

    def setDependencies( self ):
        self.buildDependencies['dev-utils/pkg-config'] = 'default'
        self.runtimeDependencies['libs/qt5/qtbase'] = 'default'
        self.runtimeDependencies['libs/qt5/qtquickcontrols'] = 'default'
        # Qt WebEngine doesn't work with MinGW, because reasons, i guess, derp
        # No DropBox support for you, until we can get that made prettier
        if not CraftCore.compiler.isMinGW():
            self.runtimeDependencies['libs/qt5/qtwebengine'] = 'default'
        self.runtimeDependencies['libs/boost/boost-system'] = 'default'
        self.runtimeDependencies['libs/lcms2'] = 'default'
        self.runtimeDependencies['libs/libgit2'] = 'default'
        self.runtimeDependencies['libs/eigen3'] = 'default'
#        self.runtimeDependencies['libs/vc'] = 'default'
        self.runtimeDependencies['kdesupport/qca'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/kcodecs'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/kconfig'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/kcoreaddons'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/kdbusaddons'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/ki18n'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/kitemviews'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/sonnet'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/threadweaver'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/kirigami'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/breeze-icons'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/kguiaddons'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/kwidgetsaddons'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier1/kwindowsystem'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier2/kdoctools'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier2/kcompletion'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier2/kjobwidgets'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/kconfigwidgets'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/kiconthemes'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/kcmutils'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/kio'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/khtml'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/kross'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/knotifications'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/knotifyconfig'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/kparts'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/ktextwidgets'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/kwallet'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier3/kxmlgui'] = 'default'
        self.runtimeDependencies['kde/frameworks/tier4/kdelibs4support'] = 'default'
        self.runtimeDependencies['extragear/kdiagram'] = 'default'

        if CraftCore.compiler.isMinGW():
            self.runtimeDependencies["libs/runtime"] = None #mingw-based builds need this

        if CraftCore.compiler.isLinux or CraftCore.compiler.isFreeBSD:
            self.runtimeDependencies["kde/frameworks/tier2/kactivities"] = None

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        CMakePackageBase.buildTests = False

    def createPackage(self):
        self.defines["appname"] = "calligragemini"
        self.defines["icon"] = os.path.join(self.sourceDir(), "gemini", "calligragemini.ico")
        self.defines["shortcuts"] = [{"name" : self.subinfo.displayName, "target":"bin/calligragemini.exe"},
                                     {"name" : "Calligra Sheets", "target" : "bin/calligrasheets.exe"},
                                     {"name" : "Calligra Words", "target" : "bin/calligrawords.exe"},
                                     {"name" : "Calligra Karbon", "target" : "bin/karbon.exe"}]
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("dev-utils/sed")

        return TypePackager.createPackage(self)
