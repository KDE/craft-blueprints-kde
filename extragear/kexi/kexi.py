import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        versions = ['3.1', 'master']
        for ver in versions:
            self.svnTargets[ver] = f"git://anongit.kde.org/kexi|{ver}"
        self.defaultTarget = versions[0]
        self.description = "A visual database applications builder"
        self.options.configure.args = " -DBUILD_EXAMPLES=ON"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["win32libs/glib"] = "default" # mdb
        self.runtimeDependencies["win32libs/sqlite"] = "default" # migration
        self.runtimeDependencies["binary/mysql"] = "default" # migration
        #TODO self.runtimeDependencies["binary/postgresql"] = "default" # migration
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebkit"] = "default"
        self.runtimeDependencies["kdesupport/kdewin"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcodecs"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/kguiaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/tier3/kconfigwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktextwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["extragear/kdb"] = "default"
        self.runtimeDependencies["extragear/kproperty"] = "default"
        self.runtimeDependencies["extragear/kreport"] = "default"
        # Desktop only:
        self.runtimeDependencies["frameworks/tier2/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktexteditor"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktextwidgets"] = "default"
        if OsUtils.isLinux():
            self.runtimeDependencies["frameworks/tier1/kcrash"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        # TODO
        #self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.defines["productname"] = "KEXI"
        self.defines["executable"] = "bin\\kexi.exe"
        #self.defines["icon"] = os.path.join(self.packageDir(), "kexi.ico")
        # TODO:  find a way to extend the default script
        #self.scriptname = os.path.join(self.packageDir(), "NullsoftInstaller.nsi")
        #self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
