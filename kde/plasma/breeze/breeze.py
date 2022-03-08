import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in self.versionInfo.tarballs():
            self.patchToApply[ver] = ('breeze-noWinDrag.diff', 0)

        self.patchToApply["5.24.3"] = [('breeze-noWinDrag.diff', 0), ('0001-Add-missing-kcoreaddons-dep.patch', 1), ('0002-Fix-build-without-QtQuick-and-QtX11Extras.patch', 1)]

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpackage"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        if not OsUtils.isWin():
            self.runtimeDependencies["kde/frameworks/tier4/frameworkintegration"] = None
        if not OsUtils.isWin() and not OsUtils.isMac():
            self.runtimeDependencies["kde/plasma/kdecoration"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if OsUtils.isWin():
            self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_KF5FrameworkIntegration=ON -DWITH_DECORATIONS=OFF"

        if OsUtils.isMac():
            self.subinfo.options.configure.args += " -DWITH_DECORATIONS=OFF"
