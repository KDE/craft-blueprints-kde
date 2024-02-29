import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in self.versionInfo.tarballs():
            self.patchToApply[ver] = ("breeze-noWinDrag.diff", 0)

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpackage"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        if not OsUtils.isWin():
            self.runtimeDependencies["kde/frameworks/tier4/frameworkintegration"] = None
        if not OsUtils.isWin() and not OsUtils.isMac():
            self.runtimeDependencies["kde/plasma/kdecoration"] = None


class Package(CraftPackageObject.get("kde/plasma").pattern):
    def __init__(self):
        super().__init__()
        if OsUtils.isWin():
            self.subinfo.options.configure.args += ["-DCMAKE_DISABLE_FIND_PACKAGE_KF5FrameworkIntegration=ON", "-DWITH_DECORATIONS=OFF"]

        if OsUtils.isMac():
            self.subinfo.options.configure.args += ["-DWITH_DECORATIONS=OFF"]

        qtMajor = CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion
        self.subinfo.options.configure.args += [f"-DBUILD_QT5={'ON' if qtMajor == '5' else 'OFF'}", f"-DBUILD_QT6={'ON' if qtMajor == '6' else 'OFF'}"]
