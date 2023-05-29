import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/atcore|master"
        self.svnTargets["1.0"] = "https://anongit.kde.org/atcore|1.0"
        self.defaultTarget = "1.0"

        self.displayName = "AtCoreTest"
        self.webpage = "https://atelier.kde.org"
        self.description = "The KDE core of Atelier Printer Host"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtserialport"] = None
        self.runtimeDependencies["libs/qt5/qtcharts"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if self.buildTarget != "1.0":
            self.subinfo.options.configure.args = "-DBUILD_GUI=ON"
            if OsUtils.isMac():
                self.subinfo.options.configure.args += "-DDEPLOY_PLUGINS_WITH_BINARY=ON"

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist.txt"))
        self.defines["executable"] = "bin\\atcore-gui.exe"
        self.defines["appname"] = "atcore-gui"
        self.defines["icon"] = os.path.join(self.packageDir(), "atcore.ico")
        return super().createPackage()
