import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply['5.57.0'] = [("disabled-deprecated-before.patch", 1)]
        self.patchToApply["5.67.0"] = [("0001-Make-kstatusnotifieritem-available-without-dbus.patch", 1), ("0001-Use-fallback-also-on-Windows-not-only-mac.patch", 1)]
        self.patchToApply["5.68.0"] = self.patchToApply["5.67.0"]
        self.patchLevel["5.67.0"] = 2


    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtspeech"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["qt-libs/phonon"] = None
        if OsUtils.isMac():
            self.runtimeDependencies["libs/qt5/qtmacextras"] = None
        if OsUtils.isWin():
            self.runtimeDependencies["dev-utils/snoretoast"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
