from distutils.dir_util import mkpath

import info
from Blueprints.CraftVersion import CraftVersion


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets[ 'master' ] = 'git://anongit.kde.org/calligra.git'
        self.defaultTarget = 'master'
        self.description = 'The Integrated Work Applications Suite by KDE'
        self.webpage = "https://calligra.org/"

    def setDependencies( self ):
        self.buildDependencies['dev-util/pkg-config'] = 'default'
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
        self.runtimeDependencies['frameworks/tier1/kcodecs'] = 'default'
        self.runtimeDependencies['frameworks/tier1/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/tier1/kcoreaddons'] = 'default'
        self.runtimeDependencies['frameworks/tier1/kdbusaddons'] = 'default'
        self.runtimeDependencies['frameworks/tier1/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/tier1/kitemviews'] = 'default'
        self.runtimeDependencies['frameworks/tier1/sonnet'] = 'default'
        self.runtimeDependencies['frameworks/tier1/threadweaver'] = 'default'
        self.runtimeDependencies['frameworks/tier1/kirigami'] = 'default'
        self.runtimeDependencies['frameworks/tier1/breeze-icons'] = 'default'
        self.runtimeDependencies['frameworks/tier1/kguiaddons'] = 'default'
        self.runtimeDependencies['frameworks/tier1/kwidgetsaddons'] = 'default'
        self.runtimeDependencies['frameworks/tier1/kwindowsystem'] = 'default'
        self.runtimeDependencies['frameworks/tier2/kdoctools'] = 'default'
        self.runtimeDependencies['frameworks/tier2/kcompletion'] = 'default'
        self.runtimeDependencies['frameworks/tier2/kjobwidgets'] = 'default'
        self.runtimeDependencies['frameworks/tier3/kactivities'] = 'default'
        self.runtimeDependencies['frameworks/tier3/kconfigwidgets'] = 'default'
        self.runtimeDependencies['frameworks/tier3/kiconthemes'] = 'default'
        self.runtimeDependencies['frameworks/tier3/kcmutils'] = 'default'
        self.runtimeDependencies['frameworks/tier3/kio'] = 'default'
        self.runtimeDependencies['frameworks/tier3/khtml'] = 'default'
        self.runtimeDependencies['frameworks/tier3/kross'] = 'default'
        self.runtimeDependencies['frameworks/tier3/knotifications'] = 'default'
        self.runtimeDependencies['frameworks/tier3/knotifyconfig'] = 'default'
        self.runtimeDependencies['frameworks/tier3/kparts'] = 'default'
        self.runtimeDependencies['frameworks/tier3/ktextwidgets'] = 'default'
        self.runtimeDependencies['frameworks/tier3/kwallet'] = 'default'
        self.runtimeDependencies['frameworks/tier3/kxmlgui'] = 'default'
        self.runtimeDependencies['frameworks/tier4/kdelibs4support'] = 'default'
        self.runtimeDependencies['extragear/kdiagram'] = 'default'

        if CraftCore.compiler.isMinGW():
            self.runtimeDependencies["libs/runtime"] = "default" #mingw-based builds need this

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        CMakePackageBase.buildTests = False

    def createPackage(self):
        self.defines["productname"] = "Calligra Gemini"
        self.defines["icon"] = os.path.join(self.sourceDir(), "gemini", "calligragemini.ico")
        self.defines["shortcuts"] = [{"name" : self.defines["productname"], "target":"bin/calligragemini.exe"},
                                     {"name" : "Calligra Sheets", "target" : "bin/calligrasheets.exe"},
                                     {"name" : "Calligra Words", "target" : "bin/calligrawords.exe"},
                                     {"name" : "Calligra Karbon", "target" : "bin/karbon.exe"},
                                     {"name" : "Calligra Plan",  "target" : "bin/calligraplan.exe"}]
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("gnuwin32/sed")

        return TypePackager.createPackage(self)


    def preArchive(self):
        archiveDir = self.archiveDir()

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
