import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/atcore|master'
        self.svnTargets['1.0'] = 'git://anongit.kde.org/atcore|1.0'
        self.defaultTarget = '1.0'

        self.displayName = "AtCoreTest"
        self.description = "The KDE core of Atelier Printer Host"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtserialport"] = "default"
        self.runtimeDependencies["libs/qt5/qtcharts"] = "default"


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_GUI=ON "
        self.subinfo.options.configure.args += "-DDEPLOY_PLUGINS_WITH_BINARY=ON "
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(self.packageDir(), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines["executable"] = "bin\\atcore-gui.exe"
        self.defines["appname"] = "atcore-gui"
        self.defines["website"] = "https://atelier.kde.org"
        self.defines["icon"] = os.path.join(self.packageDir(), "atcore.ico")

        return TypePackager.createPackage(self)

